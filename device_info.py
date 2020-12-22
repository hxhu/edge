#先下载psutil库:pip install psutil
import psutil
import os,datetime,time,platform
 
def get_cpu_use(): # cpu使用率不超过70%
    data = psutil.virtual_memory()
    cpu_use = int(psutil.cpu_percent(interval=1))

    flag = True
    if cpu_use > 70:
        flag = False

    return flag

def get_mem_use(): # mem使用率不超过80%
    data = psutil.virtual_memory()
    memory_use = int(round(data.percent))

    flag = True
    if memory_use > 80:
        flag = False

    return flag

def get_avg_load(): # 系统平均负载率
    flag = True
    if platform.system().lower() == 'linux':
        la1, la2, la3 = os.getloadavg()
        if la1 > 3 or la2 > 3 or la3 > 3:
            flag = False
    
    return flag

def total_load():  # 总负载情况
    if get_cpu_use() and get_mem_use() and get_avg_load():
        return True
    else:
        return False

def main():
 
    if total_load():
        print("True")
    else:
        print("False")
        
 
if __name__=="__main__":
    main()