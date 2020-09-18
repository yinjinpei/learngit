#-*- coding:utf-8 -*-

from git import repo

git_url='https://gitee.com/yinjinpei/learngit.git'

to_path='D:\gitpython'

remote = repo.create_remote(name='gitlab', url=git_url)


# 如果是通过clone下载的项目可直接通过repo.remote()创建remote对象
remote = repo.clone_from(git_url, to_path).remote()
