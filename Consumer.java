import java.util.Queue;

public class Consumer extends Thread{
    Queue<Integer> queue;
    int maxsize;

    Consumer(Queue<Integer> queue, int maxsize, String name){
        this.setName(name);
        this.queue = queue;
        this.maxsize = maxsize;
    }

    @Override
    public void run(){
        while(true){
            synchronized(queue){
                try{
                    Thread.sleep(1000);
                }catch(Exception e){

                }

                System.out.println(this.getName()+"获得队列的锁");
                while(queue.isEmpty()){
                    System.out.println("队列为空，消费者"+this.getName()+"进入等待");
                    try{
                        queue.wait();
                    }catch(Exception e){

                    }
                }

                int num = queue.poll();
                System.out.println("消费者"+this.getName()+"消费了"+num+"，队列中还有"+queue.size()+"个产品");
                queue.notifyAll();
                System.out.println(this.getName()+"退出消费，释放队列的锁");
            
            }
        }
    }
}
