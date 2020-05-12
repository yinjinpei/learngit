# coding:utf-8
# author:YJ沛

import os,zipfile,datetime

#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_dir,output_filename):
  zipf = zipfile.ZipFile(output_dir+'/'+output_filename, 'w')
  pre_len = len(os.path.dirname(source_dir))
  for parent, dirnames, filenames in os.walk(source_dir):
    for filename in filenames:
      pathfile = os.path.join(parent, filename)
      arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
      zipf.write(pathfile, arcname)
  zipf.close()


source_dir='zip包'
output_dir='output_zip'
output_filename='test.zip'
# make_zip(source_dir,output_dir,output_filename)

print(datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))


def test(a=None):
    if a is None:
        print('a是一个None',a)
    else:
        print('a不是空值',a)


test('123')
