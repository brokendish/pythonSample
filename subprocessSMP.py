#!/usr/bin/python
# _*_ coding: utf-8 _*_

import shlex
import subprocess as sb
import os
import sys
import re
import inspect


#BBBBBBB
#aaaaaaaaaA
#DDDDDDD
#------------------------------------------
# 標準出力、エラー出力をログファイルに出力
#------------------------------------------
def RunLog(script, out_file):
   print(inspect.currentframe().f_code.co_name + "-----Start")
   with open(out_file, 'w') as of:
      #proc = sb.Popen(shlex.split(script),env=os.environ,stdout=sb.PIPE,stderr=sb.PIPE)
      #proc = sb.Popen(shlex.split(script), stderr=sb.PIPE, stdout=sb.PIPE)
      #proc = sb.Popen(script, shell=True, stderr=sb.PIPE, stdout=sb.PIPE)
      proc = sb.Popen(script, shell=True, stderr=of, stdout=of)
   
   stdout,stderr = proc.communicate()

   ret = proc.returncode
   del proc

   print("return=%s"%ret)
   print(inspect.currentframe().f_code.co_name + "-----End")

# ------------------------------------------
# ディレクトリを作成（階層も作成） 
# [os.makedirs]はディレクトリ階層も作成するが、存在した場合は例外になる
# ------------------------------------------
def MakeDirectories(toDir):
   print(inspect.currentframe().f_code.co_name + "-----Start")
   try:
      os.makedirs(toDir)
   except FileExistsError as e:
      print("FileExists!!")
#      print('message:' + e.message)
      print("FileExists:" + str(e))
   else:
     #　例外が発生しなかった場合に通る処理
     sb.check_call("ls -la " + toDir,shell=True) 

   print(inspect.currentframe().f_code.co_name + "-----End")

# ------------------------------------------
# 文字列からプロセスIDを取得 
# Linuxコマンドの[pidof]が使える場合
# ※3系の場合は結果がバイナリで戻ってくるので
#  「universal_newlines=True」を付けると文字列で返してくれる
# ------------------------------------------
def PorcNameProcID_Popen(kwd):
   print(inspect.currentframe().f_code.co_name + "-----Start")
   shl = "pidof " + kwd	
   data = ""
   try:
      #----- popenを使う場合 ----<<余分な文字が入ってくるので使いにくい	
      #                           →proc.communicate()[0]にすればstdoutだけが帰ってくるので
      #                            余分な文字は入ってこない
      #                            proc.communicate()にすると[0]のstdoutと[1]のstderrが
      #                            帰ってくるので配列になる。今回の場合はstdoutしか使わないのでi
      #                            proc.communicate()[0]でよい
      #proc = sb.Popen(shl, shell=True, stdout=sb.PIPE)
      #print("kwd={} PID={}" .format(kwd,str(stdout_data)))
      proc = sb.Popen(shl, shell=True, stdout=sb.PIPE,universal_newlines=True)
      # タイムアウトは15秒。それ以上かかった場合は例外処理へ
      stdout_data = proc.communicate(timeout=15)[0]
      print("Popen整形前 --- kwd={} PID={}" .format(kwd,stdout_data))
      
      if len(stdout_data) > 0:
         #余分な文字を正規表現を使用して削除
         data = re.sub(r"'|\(|\|\|\)","",str(stdout_data))
         #文字列を配列に変換
         data = str(data).split(' ')
         for lines in data:
            print("Popen整形後 --- kwd={} PID={}" .format(kwd,lines))

      del proc
   except TimeoutExpired:
      proc.kill()
      stdout_data = proc.communicate()
   print(inspect.currentframe().f_code.co_name + "-----End")
   return data

# ------------------------------------------
# 文字列からプロセスIDを取得 
# Linuxコマンドの[pidof]が使える場合
# ※3系の場合は結果がバイナリで戻ってくるので
#  「universal_newlines=True」を付けると文字列で返してくれる
# ------------------------------------------
def PorcNameProcID_check_output(kwd):
   print(inspect.currentframe().f_code.co_name + "-----Start")
   shl = "pidof " + kwd	
   data = ""

   try:
      #----- check_outputを使う場合 ----<<余分な文字は入ってこないので使いやすい	
      ret = sb.check_output(shl,shell=True,universal_newlines=True)
      print("check_output整形前 --- kwd={} PID={}" .format(kwd,ret))
      if len(ret) > 0:
         #文字列を配列に変換
         data = ret.split(' ')
         for lines in data:
            print("check_output整形後 --- kwd={} PID={}" .format(kwd,lines))
   except:
      print("No Process!") 
   print(inspect.currentframe().f_code.co_name + "-----End")
   return data
      
# ------------------------------------------
# プロセスをKILL 
# os.kill:プロセスKILL
# os.killpg:子プロセスも全てKILL
# ------------------------------------------
def ProcNameKill(kwd):
   print(inspect.currentframe().f_code.co_name + "-----Start")
   #SIG = 9 #SIGKILL
   SIG = 1 #SIGHUP
   proc = PorcNameProcID_Popen(kwd)
   if len(proc) > 0:
      for pid in proc:
         print("Kill APP={} PID={}".format(kwd,pid))
         os.kill(int(pid),int(SIG))

   print(inspect.currentframe().f_code.co_name + "-----End")

#----- main -----
if __name__ == '__main__':

   # 標準出力、エラー出力をログファイルに出力
   RunLog(script="ls -la", out_file="log.txt")

   # ディレクトリを作成（階層も作成） 
   MakeDirectories(toDir="/tmp/tool/python/pythonSample/dir1/dir1-1")
   MakeDirectories(toDir="/tmp/tool/python/pythonSample/dir1/dir1-2")

   # 文字列からプロセスIDを取得 
#   PorcNameProcID(kwd="python")
#   PorcNameProcID(kwd="chrome")
   PorcNameProcID_Popen(kwd="watch")
   PorcNameProcID_check_output(kwd="watch")

   #プロセス名を指定してKILLする
   #起動プロセスは（watch --interval 0.5 ls -la
   ProcNameKill("watch")
