# README #

This README would normally document whatever steps are necessary to get your application up and running.

### Why this is not in devcontainer ###

* Because need to porforward vector store to localhost

### How do I get set up? ###

* make sure you portforward the chromadb: `kubectl port-forward service/chroma-db 17171:8000 -n algobox-default`
* enable poetry `pip install poetry`
* run the poetry install `poetry install`, if this step go wrong, probably need to do some slight change in the pyproject.toml, just help me commit..
* make sure you are in the portry shell `poetry shell`
* source credentials (make a copy of credetials.template) `cp credentials.template credentials`, then edit credentials, `source credentials`
* make up
* use any tool to post to `http://localhost:8000/apis/q-and-a/q` with question like `app/models/schemas -> class Question` 

then you have 

![nice!](/first_200_response.png)


### gunicorn default worker (sync) vs gvent worker (async)

* using one sync worker `make up_sync_one`, Using worker: sync
    * sending one request `asyncio.run(main(task_count=1, interval=0.1))`
        * client side log

            ```
            now is 536626.341128916
            executing request with process id: 13333
            executing request with thread id : 6178254848
            obtained response: 200 in 12.925236042006873 seconds
            tasks completed: 1 / 1
            ```
        
        * server side log

            ```
            api layer got it at 536912.764054291
            request handled with process id: 13236
            request handled request with thread id : 8312986432
            ```

    * sending 3 request `asyncio.run(main(task_count=3, interval=0.1))`
        * client side log

            ```
            now is 536922.755974791
            executing request with process id: 17982
            executing request with thread id : 6182858752
            now is 536922.856979125
            executing request with process id: 17982
            executing request with thread id : 6200832000
            now is 536922.958225583
            executing request with process id: 17982
            executing request with thread id : 6217658368
            obtained response: 200 in 12.437473083962686 seconds
            tasks completed: 1 / 3
            obtained response: 200 in 24.617909916094504 seconds
            tasks completed: 2 / 3
            obtained response: 200 in 37.35738104209304 seconds
            tasks completed: 3 / 3
            ```
        
        * server side log

            ```
            api layer got it at 536922.764054291
            request handled with process id: 17781
            request handled request with thread id : 8312986432
            api layer got it at 536935.193717458
            request handled with process id: 17781
            request handled request with thread id : 8312986432
            api layer got it at 536947.475344791
            request handled with process id: 17781
            request handled request with thread id : 8312986432
            ```
    
* using one sync worker `make up_sync_three`, Using worker: sync
    * sending 3 request `asyncio.run(main(task_count=3, interval=0.1))`
        * client side log
    
            ```
            now is 537154.793756666
            executing request with process id: 21652
            executing request with thread id : 6186184704
            now is 537154.894792875
            executing request with process id: 21652
            executing request with thread id : 6204157952
            now is 537154.995905833
            executing request with process id: 21652
            executing request with thread id : 6220984320
            obtained response: 200 in 13.952579207951203 seconds
            tasks completed: 1 / 3
            obtained response: 200 in 14.64842495904304 seconds
            tasks completed: 2 / 3
            obtained response: 200 in 14.510026167030446 seconds
            tasks completed: 3 / 3
            ```

        * server side log

            ```
            api layer got it at 537154.801763333
            request handled with process id: 21329
            request handled request with thread id : 8312986432
            api layer got it at 537154.898455166
            request handled with process id: 21327
            request handled request with thread id : 8312986432
            api layer got it at 537154.999077125
            request handled with process id: 21328
            request handled request with thread id : 8312986432
            ```

    * sending 6 request `asyncio.run(main(task_count=6, interval=0.1))`
        * client side log

            ```
            now is 537413.589531708
            executing request with process id: 25799
            executing request with thread id : 6179713024
            now is 537413.690519333
            executing request with process id: 25799
            executing request with thread id : 6197686272
            now is 537413.791603958
            executing request with process id: 25799
            executing request with thread id : 6214512640
            now is 537413.89297225
            executing request with process id: 25799
            executing request with thread id : 6231339008
            now is 537413.994045541
            executing request with process id: 25799
            executing request with thread id : 6248165376
            now is 537414.095180458
            executing request with process id: 25799
            executing request with thread id : 6264991744
            obtained response: 200 in 12.135760791948996 seconds
            tasks completed: 1 / 6
            obtained response: 200 in 12.874258916941471 seconds
            tasks completed: 2 / 6
            obtained response: 200 in 13.708460541907698 seconds
            tasks completed: 3 / 6
            obtained response: 200 in 23.04696154105477 seconds
            tasks completed: 4 / 6
            obtained response: 200 in 23.66787162492983 seconds
            tasks completed: 5 / 6
            obtained response: 200 in 24.338476791977882 seconds
            tasks completed: 6 / 6
            ```

        * server side log

            ```
            api layer got it at 537413.598751458
            request handled with process id: 25636
            request handled request with thread id : 8312986432
            api layer got it at 537413.694170666
            request handled with process id: 25634
            request handled request with thread id : 8312986432
            api layer got it at 537413.795231583
            request handled with process id: 25635
            request handled request with thread id : 8312986432
            api layer got it at 537425.929242916
            request handled with process id: 25635
            request handled request with thread id : 8312986432
            api layer got it at 537426.565953083
            request handled with process id: 25634
            request handled request with thread id : 8312986432
            api layer got it at 537427.298616875
            request handled with process id: 25636
            request handled request with thread id : 8312986432
            ```

* Using 3 sync worker, each 2 threads `make up_sync_three_2_threads` ,Using worker: gthread
    * sending 6 request `asyncio.run(main(task_count=6, interval=0.1))`
        * client side log

            ```
            now is 537753.19280125
            executing request with process id: 30990
            executing request with thread id : 6114242560
            now is 537753.293716541
            executing request with process id: 30990
            executing request with thread id : 6132215808
            now is 537753.394871416
            executing request with process id: 30990
            executing request with thread id : 6149042176
            now is 537753.496008708
            executing request with process id: 30990
            executing request with thread id : 6165868544
            now is 537753.597164333
            executing request with process id: 30990
            executing request with thread id : 6182694912
            now is 537753.698295791
            executing request with process id: 30990
            executing request with thread id : 6199521280
            obtained response: 200 in 14.439501540968195 seconds
            tasks completed: 1 / 6
            obtained response: 200 in 15.002718208939768 seconds
            tasks completed: 2 / 6
            obtained response: 200 in 15.160724707995541 seconds
            tasks completed: 3 / 6
            obtained response: 200 in 15.52860924997367 seconds
            tasks completed: 4 / 6
            obtained response: 200 in 15.782448249985464 seconds
            tasks completed: 5 / 6
            obtained response: 200 in 27.216284958994947 seconds
            tasks completed: 6 / 6
            ```
        
        * server side log

            ```
            api layer got it at 537753.202869125
            request handled with process id: 28995
            request handled request with thread id : 11953795072
            api layer got it at 537753.30146225
            request handled with process id: 28994
            request handled request with thread id : 11953795072
            api layer got it at 537753.400769291
            request handled with process id: 28993
            request handled request with thread id : 11534364672
            api layer got it at 537753.499064833
            request handled with process id: 28994
            request handled request with thread id : 11994804224
            api layer got it at 537753.601363375
            request handled with process id: 28995
            request handled request with thread id : 11994804224
            api layer got it at 537769.025240916
            request handled with process id: 28994
            request handled request with thread id : 11994804224
            ```

* Using 1 async worker, `make up_async_one`, Using worker: gevent
    * sending 6 request `asyncio.run(main(task_count=6, interval=0.1))`
        * client side log

            ```
            now is 538114.311999458
            executing request with process id: 36792
            executing request with thread id : 6117535744
            now is 538114.413241416
            executing request with process id: 36792
            executing request with thread id : 6135508992
            now is 538114.514108958
            executing request with process id: 36792
            executing request with thread id : 6152335360
            now is 538114.614928916
            executing request with process id: 36792
            executing request with thread id : 6169161728
            now is 538114.716792916
            executing request with process id: 36792
            executing request with thread id : 6185988096
            now is 538114.817165125
            executing request with process id: 36792
            executing request with thread id : 6202814464
            obtained response: 200 in 16.192705792025663 seconds
            tasks completed: 1 / 6
            obtained response: 200 in 16.133315709070303 seconds
            tasks completed: 2 / 6
            obtained response: 200 in 16.354080624994822 seconds
            tasks completed: 3 / 6
            obtained response: 200 in 16.659855833044276 seconds
            tasks completed: 4 / 6
            obtained response: 200 in 16.46651712502353 seconds
            tasks completed: 5 / 6
            obtained response: 200 in 17.5213071659673 seconds
            tasks completed: 6 / 6
            ```

        * server side log

            ```
            api layer got it at 538114.31811775
            request handled with process id: 36663
            request handled request with thread id : 4403862624
            api layer got it at 538114.416564458
            request handled with process id: 36663
            request handled request with thread id : 11834688832
            api layer got it at 538114.518183958
            request handled with process id: 36663
            request handled request with thread id : 11834882496
            api layer got it at 538114.625796208
            request handled with process id: 36663
            request handled request with thread id : 11834688032
            api layer got it at 538114.729125375
            request handled with process id: 36663
            request handled request with thread id : 11834882976
            api layer got it at 538114.820335791
            request handled with process id: 36663
            request handled request with thread id : 11834883776
            ```

* Using 3 async worker, `make up_async_three`, Using worker: gevent
    * sending 20 request, here i used internal at 0.01 `asyncio.run(main(task_count=20, interval=0.01))`
        * client side log:

            ```
            now is 538284.881960791
            executing request with process id: 39552
            executing request with thread id : 6182629376
            now is 538284.98271625
            executing request with process id: 39552
            executing request with thread id : 6200602624
            now is 538285.083833375
            executing request with process id: 39552
            executing request with thread id : 6217428992
            now is 538285.185180666
            executing request with process id: 39552
            executing request with thread id : 6234255360
            now is 538285.286232333
            executing request with process id: 39552
            executing request with thread id : 6251081728
            now is 538285.387433958
            executing request with process id: 39552
            executing request with thread id : 6267908096
            now is 538285.488726041
            executing request with process id: 39552
            executing request with thread id : 6284734464
            now is 538285.589678208
            executing request with process id: 39552
            executing request with thread id : 6301560832
            now is 538285.690769166
            executing request with process id: 39552
            executing request with thread id : 6318387200
            now is 538285.791900208
            executing request with process id: 39552
            executing request with thread id : 6335213568
            now is 538285.892953291
            executing request with process id: 39552
            executing request with thread id : 6352039936
            now is 538285.994086666
            executing request with process id: 39552
            executing request with thread id : 6368866304
            now is 538286.095109916
            executing request with process id: 39552
            executing request with thread id : 6385692672
            now is 538286.195472666
            executing request with process id: 39552
            executing request with thread id : 6402519040
            now is 538286.296538666
            executing request with process id: 39552
            executing request with thread id : 6419345408
            now is 538286.39782175
            executing request with process id: 39552
            executing request with thread id : 6436171776
            obtained response: 200 in 16.880364292068407 seconds
            now is 538301.76255425
            executing request with process id: 39552
            executing request with thread id : 6182629376
            tasks completed: 1 / 20
            obtained response: 200 in 23.283920207992196 seconds
            now is 538308.266947625
            executing request with process id: 39552
            executing request with thread id : 6200602624
            tasks completed: 2 / 20
            obtained response: 200 in 24.262230249936692 seconds
            now is 538309.346164791
            executing request with process id: 39552
            executing request with thread id : 6217428992
            tasks completed: 3 / 20
            obtained response: 200 in 24.813660000101663 seconds
            now is 538310.909076541
            executing request with process id: 39552
            executing request with thread id : 6385692672
            tasks completed: 4 / 20
            obtained response: 200 in 25.62001287494786 seconds
            tasks completed: 5 / 20
            obtained response: 200 in 25.969666166929528 seconds
            tasks completed: 6 / 20
            obtained response: 200 in 26.200478624901734 seconds
            tasks completed: 7 / 20
            obtained response: 200 in 25.454239874961786 seconds
            obtained response: 200 in 25.656709208036773 seconds
            tasks completed: 8 / 20
            tasks completed: 9 / 20
            obtained response: 200 in 25.396487625082955 seconds
            tasks completed: 10 / 20
            obtained response: 200 in 26.002553042024374 seconds
            tasks completed: 11 / 20
            obtained response: 200 in 26.324815582949668 seconds
            tasks completed: 12 / 20
            obtained response: 200 in 26.231689666979946 seconds
            tasks completed: 13 / 20
            obtained response: 200 in 25.390315040946007 seconds
            tasks completed: 14 / 20
            obtained response: 200 in 25.843176375026815 seconds
            tasks completed: 15 / 20
            obtained response: 200 in 26.532001000014134 seconds
            tasks completed: 16 / 20
            obtained response: 200 in 12.896951541071758 seconds
            tasks completed: 17 / 20
            obtained response: 200 in 12.26313870807644 seconds
            tasks completed: 18 / 20
            obtained response: 200 in 11.250063791987486 seconds
            tasks completed: 19 / 20
            obtained response: 200 in 12.583383792079985 seconds
            tasks completed: 20 / 20
            ```

        * server side log:

            ```
            api layer got it at 538284.888915666
            request handled with process id: 38726
            request handled request with thread id : 11712732416
            api layer got it at 538284.985177791
            request handled with process id: 38726
            request handled request with thread id : 4800657856
            api layer got it at 538285.086373666
            request handled with process id: 38726
            request handled request with thread id : 11713295712
            api layer got it at 538285.187806541
            request handled with process id: 38726
            request handled request with thread id : 11713284032
            api layer got it at 538285.289270166
            request handled with process id: 38726
            request handled request with thread id : 11713086464
            api layer got it at 538285.390630041
            request handled with process id: 38726
            request handled request with thread id : 11713298112
            api layer got it at 538285.49253925
            request handled with process id: 38724
            request handled request with thread id : 11722261504
            api layer got it at 538285.592684166
            request handled with process id: 38724
            request handled request with thread id : 11722443008
            api layer got it at 538285.694418166
            request handled with process id: 38724
            request handled request with thread id : 11722455328
            api layer got it at 538285.794158958
            request handled with process id: 38724
            request handled request with thread id : 11722456448
            api layer got it at 538285.895098541
            request handled with process id: 38724
            request handled request with thread id : 11722261344
            api layer got it at 538285.996872583
            request handled with process id: 38725
            request handled request with thread id : 11716232832
            api layer got it at 538286.097081583
            request handled with process id: 38725
            request handled request with thread id : 11715871904
            api layer got it at 538286.197546916
            request handled with process id: 38726
            request handled request with thread id : 11713612032
            api layer got it at 538286.299498333
            request handled with process id: 38725
            request handled request with thread id : 11716443680
            api layer got it at 538286.400497875
            request handled with process id: 38726
            request handled request with thread id : 11713613632
            api layer got it at 538301.766921833
            request handled with process id: 38726
            request handled request with thread id : 4356283648
            api layer got it at 538308.271251166
            request handled with process id: 38726
            request handled request with thread id : 4800657856
            api layer got it at 538309.349401458
            request handled with process id: 38726
            request handled request with thread id : 11713295712
            api layer got it at 538310.914413333
            request handled with process id: 38726
            request handled request with thread id : 11713625632
            ```

### Lesson leanrt above tests

* One gunicorn sync worker, can only do 1 task at a time, here we have the benchmark of how long one request should take.
* Three gunicorn sync workers, can do 3 tasks at a time (each one has a different process id). based on gunicorn documents, the number of workers is recommended to be (number of cpu * 2) + 1. 
* Three gunicorn sync workers, can do up to 6 tasks at a time (we now have a permunation of 3 processes and 2 fixed thread ids, each processes make uses of the 2 thread id. please take note that, it is 6 threads!, not just 2, gunicorn just name them same, i guess). However, the server only did 5 tasks in one shot, and the 6th task is done in the second batch!!!. I am not really sure why.. could it be contraint in memory? i am not sure how big are the stuff created in memory or cpu.., but definitely, the requests are getting slower. in the first batch, each requests takes about 15 seconds! the last one goes along, takes 12 seconds. Thus I feel, this is not only IO bound task, but there is something CPU bound as well.
* One gevent worker. can do 6 tasks together. The server uses one process id with 6 threads. but each takes 16 to 17 seconds to finish.
* Three gevent worker. Here I send in 20 tasks together. The server finished 16 on them at about 24 seconds mark, utilizing 3 process id with all different threads number. THen did the last 4 in 12 seconds. THe first of the last 4 is sent after the first 1 of the 20 get completed. It looks like it is a client's issue, which only can send up to 16 requests in one shot. Here we can see that, in terms of responding time, 16 requests is definitely slower than doing 6 requests, but still, better than doing 6 requests in 3 batches... the 16 feels like a weird contraint on hardware..
* Thus a final test is done as below, with 3 async workers, and 2 more lines added to `async def main`: so that subsequent calls to to_thread will now use an executor with a thread limit of 200.

    * 2 lines added before create_task, where `execute_single_task` uses asyncio.to_thread, which is actually a wrapper around ThreadPoolExecutor. The default number of threads is: `Total Number Worker Threads = (CPUs in Your System) + 4` and here my mac book pro (M2, 16inch) has 12 cpus. Thus 16. However we can change this number by the 2 lines below.
        ```
        loop = asyncio.get_running_loop()
        loop.set_default_executor(ThreadPoolExecutor(max_workers=200))

        # below chunk will use to_thread!
        for i in range(task_count):
            task = asyncio.create_task(execute_single_task(i=i, mock=mock))
            tasks.append(task)
        ```
    
    * now sending 20 questions to answer is processed together, client side log is below. The servier side is 20 requests, arriving at api laer with 0.1s internal, processed by 3 processes (20 threads) 

        ```
        this is request 0, now is 543429.795030833
        executing request with process id: 23143
        executing request with thread id : 6110605312
        this is request 1, now is 543429.896404708
        executing request with process id: 23143
        executing request with thread id : 6128578560
        this is request 2, now is 543429.997615625
        executing request with process id: 23143
        executing request with thread id : 6145404928
        this is request 3, now is 543430.098893583
        executing request with process id: 23143
        executing request with thread id : 6162231296
        this is request 4, now is 543430.199859875
        executing request with process id: 23143
        executing request with thread id : 6179057664
        this is request 5, now is 543430.300966166
        executing request with process id: 23143
        executing request with thread id : 6195884032
        this is request 6, now is 543430.402159916
        executing request with process id: 23143
        executing request with thread id : 6212710400
        this is request 7, now is 543430.502680291
        executing request with process id: 23143
        executing request with thread id : 6229536768
        this is request 8, now is 543430.603787375
        executing request with process id: 23143
        executing request with thread id : 6246363136
        this is request 9, now is 543430.704929625
        executing request with process id: 23143
        executing request with thread id : 6263189504
        this is request 10, now is 543430.806720291
        executing request with process id: 23143
        executing request with thread id : 6280015872
        this is request 11, now is 543430.907187375
        executing request with process id: 23143
        executing request with thread id : 6296842240
        this is request 12, now is 543431.008240291
        executing request with process id: 23143
        executing request with thread id : 6313668608
        this is request 13, now is 543431.109065375
        executing request with process id: 23143
        executing request with thread id : 6330494976
        this is request 14, now is 543431.210227958
        executing request with process id: 23143
        executing request with thread id : 6347321344
        this is request 15, now is 543431.3107705
        executing request with process id: 23143
        executing request with thread id : 6364147712
        this is request 16, now is 543431.411836458
        executing request with process id: 23143
        executing request with thread id : 6380974080
        this is request 17, now is 543431.513112916
        executing request with process id: 23143
        executing request with thread id : 6397800448
        this is request 18, now is 543431.614189333
        executing request with process id: 23143
        executing request with thread id : 6414626816
        this is request 19, now is 543431.715205458
        executing request with process id: 23143
        executing request with thread id : 6431453184
        obtained response for request 0: 200 in 27.30583291698713 seconds
        obtained response for request 1: 200 in 28.129415457951836 seconds
        obtained response for request 3: 200 in 28.336316999979317 seconds
        obtained response for request 16: 200 in 27.638317374978215 seconds
        obtained response for request 10: 200 in 29.576254667015746 seconds
        obtained response for request 9: 200 in 29.680734833003953 seconds
        obtained response for request 15: 200 in 29.09298979106825 seconds
        obtained response for request 6: 200 in 30.050111416960135 seconds
        obtained response for request 2: 200 in 30.53631300001871 seconds
        obtained response for request 5: 200 in 30.38886404200457 seconds
        obtained response for request 11: 200 in 29.904248540988192 seconds
        obtained response for request 19: 200 in 29.108827749965712 seconds
        obtained response for request 13: 200 in 30.09238879091572 seconds
        obtained response for request 14: 200 in 30.000539082917385 seconds
        obtained response for request 17: 200 in 29.782759750029072 seconds
        obtained response for request 8: 200 in 30.875994040980004 seconds
        obtained response for request 4: 200 in 31.3282921659993 seconds
        obtained response for request 18: 200 in 29.94519199989736 seconds
        obtained response for request 12: 200 in 30.666848208988085 seconds
        obtained response for request 7: 200 in 32.23045216698665 seconds
        ```


    


### Notes on LLM

*
*