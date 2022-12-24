import java.util.Queue;
public class Producer extends Thread{
    Queue<Integer> queue;
    int maxsize;

    Producer(Queue<Integer> queue, int maxsize, String name){
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

                while(queue.size() == maxsize){
                    System.out.println("队列已满，生产者"+this.getName()+"进入等待");
                    try{
                        queue.wait();
                    }catch(Exception e){
                        
                    }
                }

                int num = (int) (Math.random()*100);
                queue.offer(num);

                System.out.println("生产者"+this.getName()+"生产了"+num+"，队列中还有"+queue.size()+"个产品");
                queue.notifyAll();

                System.out.println(this.getName()+"退出生产，释放队列的锁");
            }
        }
    }
}
