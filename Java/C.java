
/* Check if the input is pangram or not. (Pangram is a sentence that contains all the alphabet
from a-z) */

public class PangramChecker {
    public static boolean isPangram(String str) {
        boolean[] letters = new boolean[26];
        str = str.toLowerCase();

        for (int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);

            if (c >= 'a' && c <= 'z') {
                int index = c - 'a';
                letters[index] = true;
            }
        }

        for (boolean present : letters) {
            if (!present) {
                return false;
            }
        }

        return true;
    }

    public static void main(String[] args) {
        String input = "The quick brown fox jumps over the lazy dog";
        boolean isPangram = isPangram(input);
        if (isPangram) {
            System.out.println("The input is a pangram.");
        } else {
            System.out.println("The input is not a pangram.");
        }
    }
}
