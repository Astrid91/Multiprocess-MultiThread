from time import time
from multiprocessing import Process, Queue
import threading
from datetime import datetime, timedelta

def Bubblesort( data ):
    n = len( data )
    for i in range( n ):
        for j in range( 0, n-i-1 ):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]

    return data

def Merge( left, right ):
    sorted = []
    while len( left ) != 0 and len( right ) != 0:
        if ( left[0] > right[0] ):
            sorted.append( right.pop(0) )
        else:
            sorted.append( left.pop(0) )

    if ( len(left) != 0 ):       # 把剩下沒排完的陣列加入sorted
        sorted += left
    else:
        sorted += right
    return sorted

def Mission1( data, result_queue, i ) :
    result_queue.put( Bubblesort( data[i] ) )

def Mission3( data, index, result_queue ):
    data[0] = Merge(data[0], data[index])
    result_queue.put(data[0])

def HandleMethod( method, data, K ):
    result_queue = Queue()
    start = time()
    if method == 1:
        Mission1( data, result_queue, 0 )
        result = result_queue.get()

    elif method == 2:
        for index in range(K):  # 要做K次 bubble sort
            Bubblesort(data[index])  # 將排序好的存回 data

        for i in range(1, K):  # 每兩筆合併
            data[0] = Merge(data[0], data[i])  # 進行 merge_sort

        result = data[0]

    elif method == 3:
        processes = []
        for i in range(K):
            process = Process( target = Mission1, args = ( data, result_queue, i ) )
            processes.append(process)
            process.start()
            data[i] = result_queue.get()
            process.join()

        for i in range(K-1):
            process = Process( target=Mission3, args=(data, i+1, result_queue ) )
            processes.append(process)
            process.start()
            if i+1 != K-1:
                data[0] = result_queue.get()

        result = result_queue.get()

    elif method == 4:
        queues=[]
        threads = []
        for i in range(K):
            result_queue = Queue()
            queues.append(result_queue)
            thread = threading.Thread( target = Mission1, args = ( data, result_queue, i ) )
            threads.append(thread)
            thread.start()

        # 等待所有進程結束，並且將排序後的結果收集起來
        results = []
        for i in range(K):
            threads[i].join()
            results.append(queues[i].get())

        # 用K-1個進程進行Mergesort
        for i in range(K - 1):
            thread = threading.Thread( target=Mission3, args=(results, i+1, result_queue ) )
            threads.append(thread)
            thread.start()
            if i+1 != K-1:
                results[0] = result_queue.get()

        result = result_queue.get()

    end = time()
    runtime = end - start

    return result, runtime

def ReadFile( fileName, K, method ):
    f = open( fileName, 'r' )
    lines = len( f.readlines()) # 獲取行數
    f.close()
    f = open( fileName, 'r' )
    if method == 1:
        K = 1
    count = int( lines/K )
    if lines % K != 0:
        count = count + 1
    data = [[] * count for i in range(K)]  # 宣告二維陣列
    
    for i in range(K):
        for j in range(count):
            if lines == (i*count)+j:  # 到檔案末端
                break

            temp = f.readline()
            data[i].append( int(temp) )

    f.close()
    return data

def WriteFile( fileName, method, result, runtime ):
    fileName = fileName + "_output" + str(method)
    f = open( fileName, "w" )

    print('Sort :', file=f)

    for i in range(len(result)):
        print( '%s' % str(result[i]), file = f )
        
    print( 'CPU Time : %f' % runtime, file = f )

    now_time = datetime.now()  # 獲取UTC time
    utc_time = now_time - timedelta(hours=8)  # 减去8小时
    utc_time = utc_time.strftime( "%Y-%m-%d %H:%M:%S.%f+08:00" )
    print( 'Output Time : ' + utc_time , file = f )
    f.close()

if __name__ == '__main__':
    while 1:
        fileName = input( "請輸入檔案名稱:\n" )
        K = int( input( "請輸入要切成幾份:\n" ) )
        method = int( input( "請輸入方法編號:(方法1, 方法2, 方法3, 方法4)\n" ) )

        fileName = fileName + ".txt" ;
        data = ReadFile( fileName, K, method )
        result, runtime = HandleMethod( method, data, K )
        WriteFile( fileName, method, result, runtime )
