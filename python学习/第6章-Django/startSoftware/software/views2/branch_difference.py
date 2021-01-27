import logging
import time
import json
from django.contrib import admin
from django.urls import path
from ..models import *
from threading import Thread
from django.shortcuts import render
from ..views import request_gitlab_api
from ..views import getConfig



# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")

def branch_difference(request):
    if not request.session.get('is_login', None):
        return render(request, 'software/index.html')

    # 获取该用户下的所有领域名
    domain_file = 'config/domain_config/%s_domain_config.ini' % request.session['user_name']
    read_domain = getConfig(domain_file)
    domain_list = read_domain.get_section()
    domain_list2 = read_domain.get_section()    # 用在访问令牌
    domain_list.insert(0,"")

    if request.method == 'POST':
        # 获取领域，获取相应领域的projectid、branch信息
        if request.POST.get('options') == "select_domain":
            domain_name=request.POST.get('domain_name')
            domain_list.remove(domain_name) # 去除已被选择的项
            domain_list[0]=domain_name  # 替换第一个元素，将已被选择的项显示在前端选择项中的第一个位置
            try:
                privatekey = read_domain.get_value(domain_name, 'privatekey')  # 获取用户访问gitlab访问令牌
            except:
                privatekey = None
            try:
                projectid_str = read_domain.get_value(domain_name, 'projectid')  # 获取项目ID列表
                projectid_list = projectid_str.split(',')
            except:
                projectid_str = None
                projectid_list = []

            if projectid_list and privatekey:
                project_id=projectid_list[0]
                service_name = '/repository/branches'
                get_branchInfo = request_gitlab_api(project_id, service_name, privatekey)
                branch_info = get_branchInfo.get_gitlab_branch()
                # print(branch_info)
                if json.loads(branch_info)["status_code"] == 200:
                    branch_list = json.loads(branch_info)["data"]["barnch_list"]  # 字符串转字典
            else:
                message="访问令牌或项目id无效，请检查录入资料的正确性！"

        # 判断领域下所有project id下的两个分支代码是否相同
        elif request.POST.get('options') == "get_difference_info":
            domain_name = request.POST.get('domain_name')
            source_branch = request.POST.get('source_branch')
            target_branch = request.POST.get('target_branch')
            service_name = '/repository/commits'

            try:
                privatekey = read_domain.get_value(domain_name, 'privatekey')  # 获取用户访问gitlab访问令牌
            except:
                privatekey = None
            try:
                projectid_str = read_domain.get_value(domain_name, 'projectid')  # 获取项目ID列表
                projectid_list = projectid_str.split(',')
            except:
                projectid_str = None
                projectid_list = []

            all_branch_diff_info_list=[]    # 储存所有project id比较结果
            branch_diff_info_dict={}    # 储存单个project id比较结果
            if projectid_list and privatekey:

                #######  多线程 starting ########
                def branch_diff_function(projectId,service_name,privatekey,source_branch,target_branch):
                    get_projectInfo = request_gitlab_api(projectId, service_name, privatekey)
                    branch_diff = get_projectInfo.checkout_branch_commit(source_branch, target_branch)
                    project_http_url = get_projectInfo.get_projectInfo_by_id()

                    try:
                        status_code=json.loads(branch_diff)["status_code"]
                    except Exception as e:
                        print(e)
                        status_code = 404

                    try:
                        project_http_url = json.loads(project_http_url)["data"]["http_url"]
                    except Exception as e:
                        print(e)
                        print(json.loads(project_http_url))
                        project_http_url = None

                    try:
                        result = json.loads(branch_diff)["message"]
                    except Exception as e:
                        print(e)
                        result = e

                    # print(project_http_url)
                    # print(json.loads(branch_diff))
                    branch_diff_info_dict = {"project_id": projectId,
                                             "status_code":status_code,
                                             "project_http_url": project_http_url,
                                             "source_branch": source_branch,
                                             "target_branch": target_branch,
                                             "result": result}
                    all_branch_diff_info_list.append(branch_diff_info_dict)

                thread_list = []  # 储存将要生成的所有线程
                for projectId in projectid_list:
                    t = Thread(target=branch_diff_function,
                               args=(projectId, service_name, privatekey, source_branch, target_branch))
                    t.start()   # 执行线程
                    thread_list.append(t)   # 保存线程对象

                # 等待所有线程结束
                for thread in thread_list:
                    thread.join()

                #######  多线程 end ########

            # print(all_branch_diff_info_list)

        # 查询项目信息功能
        elif request.POST.get('options') == "select_project":
            domain_name=request.POST.get('projectKeyOrDomain')
            if domain_name[-5:] == "token":
                try:
                    privatekey = read_domain.get_value(domain_name[:-7], 'privatekey')  # 获取用户访问gitlab访问令牌
                except:
                    privatekey = None
            else:
                privatekey = request.POST.get('projectKeyOrDomain')

            context = request.POST.get('context')
            context = context.replace(" ", "")  # 去空格
            context = context.replace("，", ",")  # 中文逗号转英文逗号
            context_list = context.split(",")  # 分割
            service_name = '/repository/commits'

            projectInfo_list = []  # 储存所有projectInfo结果

            def get_projectNameAndUrlByid(projectId, service_name, privatekey):
                get_projectInfo = request_gitlab_api(projectId, service_name, privatekey)
                projectInfo = get_projectInfo.get_projectInfo_by_id()
                # print(projectInfo)
                # print(json.loads(projectInfo)["data"])
                projectInfo_list.append(json.loads(projectInfo)["data"])

            def get_projectNameAndUrlByName(projectName, service_name, privatekey):
                projectId = 15104   # 此id无实际作用，只是传参
                get_projectInfo = request_gitlab_api(projectId, service_name, privatekey)
                projectInfo = get_projectInfo.get_projectInfo_by_name(projectName)
                # print(projectInfo)
                # print(json.loads(projectInfo))
                # print(json.loads(projectInfo)["data"])

                for project in json.loads(projectInfo)["data"]["projectInfo_list"]:
                    # print("#############################",project)
                    projectInfo_list.append(project)

            thread_list = []  # 储存将要生成的所有线程
            if request.POST.get('projectId_or_projectName') == "projectId":
                for projectId in context_list:
                    t = Thread(target=get_projectNameAndUrlByid, args=(projectId, service_name, privatekey))
                    t.start()  # 执行线程
                    thread_list.append(t)  # 保存线程对象

                # 等待所有线程结束
                for thread in thread_list:
                    thread.join()

            elif request.POST.get('projectId_or_projectName') == "projectName":
                for projectName in context_list:
                    t = Thread(target=get_projectNameAndUrlByName, args=(projectName, service_name, privatekey))
                    t.start()  # 执行线程
                    thread_list.append(t)  # 保存线程对象

                    # 等待所有线程结束
                for thread in thread_list:
                    thread.join()
            else:
                print("查询选择有误，请重新选择！")
                message = "查询选择有误，请重新选择！"

            # print(projectInfo_list)
    return render(request, 'software/branch_difference.html', locals())