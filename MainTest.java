import java.util.LinkedList;
import java.util.Queue;
public class MainTest {
    public static void main(String[] args){
        Queue<Integer> queue = new LinkedList<>();
        int maxsize = 2;
        Producer producer = new Producer(queue, maxsize, "生产者1");
        Producer producer2 = new Producer(queue, maxsize, "生产者2");
        Consumer consumer = new Consumer(queue, maxsize, "消费者1");
        Consumer consumer2 = new Consumer(queue, maxsize, "消费者2");
        producer.start();
        producer2.start();
        consumer.start();
        consumer2.start();
    }
}
