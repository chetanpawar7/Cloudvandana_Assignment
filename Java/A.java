//Create an array with the values (1, 2, 3, 4, 5, 6, 7) and shuffle it
import java.util.Random;

public class ArrayShuffler {
    public static void main(String[] args) {
        int[] originalArray = {1, 2, 3, 4, 5, 6, 7};
        
        shuffleArray(originalArray);
        
        System.out.print("Shuffled Array: ");
        for (int num : originalArray) {
            System.out.print(num + " ");
        }
    }

    public static void shuffleArray(int[] array) {
        Random rand = new Random();
        int n = array.length;

        for (int i = n - 1; i > 0; i--) {
            int j = rand.nextInt(i + 1);
            swap(array, i, j);
        }
    }

    public static void swap(int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}
