# Multiprocess-MultiThread

分別讀入檔名、K 值，以及方法編號，根據方法編號執行以下四種不同的
方法進行資料排序。
### 方法一：將 N 筆資料直接進行 BubbleSort，並顯示 CPU 執行之時間。 
將 N 筆資料從檔案內讀入後，存入 list 中，並直接使用當前的 process 進
行 BubbleSort，將排序結果寫入指定檔名的檔案中，並印出 CPU 的執行時
間，以及當前的 UTC 時間。
### 方法二：將 N 筆資料切成 K 份，先在一個 process 內對 K 份資料進行BubbleSort 之後，再用同一個 process 做 MergeSort，並顯示 CPU 執行之時間。 
 根據 K 值，將 N 筆資料平分切成 K 份，存入二維串列(list)中，創建出一
個新的 process，分別將 K 份資料進行 BubbleSort 後，再同樣使用相同的
process 進行 MergeSort，將結果存入 Queue 當中。寫檔時，取得 Queue 裡
面的排序結果，並印出 CPU 的執行時間，以及當前的 UTC 時間。
### 方法三：將 N 筆資料切成 K 份，並由 K 個 processes 各別進行 BubbleSort之後，再用 K-1 個 process(es)作 MergeSort，並顯示 CPU 執行之時間。 
根據 K 值，將 N 筆資料平分切成 K 份，存入二維串列(list)中，使用 for
迴圈創建出 K 個新的 process，每個 process 先對 N/K 筆資料進行
BubbleSort，並將結果存入名為 queues 的 list 中，接著使用 for 迴圈創
建出 K-1 個 process，將 K 份已排序過的資料，使用 MergeSort 再整合成
完整的一份排序資料，並將最後的結果存入 Queue 當中。寫檔時，取得
Queue 裡面的排序結果，並印出 CPU 的執行時 間，以及當前的 UTC 時間。
### 方法四：將 N 筆資料切成 K 份，並由 K 個 threads 各別進行 Bubblesort 之後，再用 K-1 個 thread(s)作 Mergesort，並顯示 CPU 執行之時間。 
 方法四和方法三類似，差別只在於方法三是使用 multiprocessing 的方式
進行資料排序，而方法四則是使用 multithreading 的方式，兩者在實作方
法上差異不大。
