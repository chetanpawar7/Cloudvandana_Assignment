/* . Take a sentence as an input and reverse every word in that sentence.
a. Example - This is a sunny day > shiT si a ynnus yad.  */

function reverseWord(word) {
    let reversedWord = '';
    for (let i = word.length - 1; i >= 0; i--) {
        reversedWord += word[i];
    }
    return reversedWord;
}

function reverseSentenceWords(sentence) {
    const words = sentence.split(' ');
    let reversedSentence = '';

    for (let i = 0; i < words.length; i++) {
        if (i > 0) {
            reversedSentence += ' ';
        }
        reversedSentence += reverseWord(words[i]);
    }

    return reversedSentence;
}

const inputSentence = 'This is a sunny day';
const reversed = reverseSentenceWords(inputSentence);
console.log(reversed);
