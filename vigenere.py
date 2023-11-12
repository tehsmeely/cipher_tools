import random
import string
import math


freqs_memo = None
def load_quadgram_freqs():
    global freqs_memo
    if freqs_memo is not None:
        return freqs_memo
    counts = {}
    with open("english_quadgrams_log.txt", "r") as f:
        for line in f:
            line = line.strip()
            txt, freq = line.split(",")
            freq = float(freq)
            counts[txt] = freq
    
    freqs_memo = counts  
    return counts


def fitness(text):
    # fitness = (1/N) * Sum of (with i from 1 to N) : log10(frequency of ith quadgram)
    freqs = load_quadgram_freqs()

    ngram_size = 4
    big_negative_number = -15.0

    result = 0
    for i in range(len(text) - (ngram_size - 1)):
        ngram = text[i:i+ngram_size]

        if ngram in freqs:
            result += freqs[ngram]
        else:
            result += big_negative_number

    return result / len(text)


def get_letter_counts(text):
    counts = {}
    for letter in text:
        if letter not in counts:
            counts[letter] = 0
        counts[letter] += 1
    return counts
def index_of_coincidence(text):
    # I = ( Sum of (with i from A - Z) : n_i * (n_i - 1) )  / (N * (N - 1))
    # where ni are counts of letter i and N is total number of letters
    N = len(text)
    other_n = 0
    letter_counts = get_letter_counts(text)
    sum = 0
    for letter in string.ascii_uppercase:
        n_i = letter_counts.get(letter, 0)
        sum += n_i * (n_i - 1)
        other_n += n_i

    if other_n != N:
        raise Exception("ERROR: N != other_n")

    divisor = N * (N - 1) if N > 1 else 1
    return 26.0 * float(sum) / divisor

def find_key_size(text):
    for period in range(2, 31):
        # slice text into slice_size chunks
        # calculate average index of coincidence
        # store in list
        slices = [''] * period 
        for i in range(len(text)):
            slices[i % period] += text[i]
        avg_ic = sum(index_of_coincidence(s) for s in slices) / period

        if avg_ic > 1.6:
            return period


def encrypt(plaintext, key):
    output = ""
    for i in range(len(plaintext)):
        p = string.ascii_uppercase.index(plaintext[i])
        k = string.ascii_uppercase.index(key[i % len(key)])
        c = (p + k) % 26
        output += string.ascii_uppercase[c]
    return output

def decrypt(ciphertext, key):
    output = ""
    for i in range(len(ciphertext)):
        p = string.ascii_uppercase.index(ciphertext[i])
        k = string.ascii_uppercase.index(key[i % len(key)])
        c = (p - k) % 26
        output += string.ascii_uppercase[c]
    return output


example_text = "The reason that the rich were so rich, Vimes reasoned, was because they managed to spend less money.Take boots, for example. He earned thirty-eight dollars a month plus allowances. A really good pair of leather boots cost fifty dollars. But an affordable pair of boots, which were sort of OK for a season or two and then leaked like hell when the cardboard gave out, cost about ten dollars. Those were the kind of boots Vimes always bought, and wore until the soles were so thin that he could tell where he was in Ankh-Morpork on a foggy night by the feel of the cobbles.But the thing was that good boots lasted for years and years. A man who could afford fifty dollars had a pair of boots that'd still be keeping his feet dry in ten years' time, while the poor man who could only afford cheap boots would have spent a hundred dollars on boots in the same time and would still have wet feet. This was the Captain Samuel Vimes 'Boots' theory of socioeconomic unfairness"
example_text = "".join([c.upper() for c in example_text if c in string.ascii_letters])
key = "GNUTP"


real_text="YOHAPIEVFWWIZBUNWVGJTMZKYFTNIIURDGVIAIRTTNAIJJDOCIJCZWMJYJIIQEOHVWANYZSGHSRGOPHKMEICKJTCOKIRRVZYEYWJHOQSIJDDBKMEWWEIIIUFKTCSSTOFTFZNYPPNSGSJXBJRPNCVBETTNSVMORMFZCJICITCWEPIRCLQDFBFBAIMKMIIURGOPHZYAIRZKIIRZYESHIJMZZPZNGWBJLTHYFTDHTTUGRYFVZPVJNRFZYTZBSDAIMFSEDBDDHJIJJHJZUDOPFTQADAKMAOHYJCCOIFCOSINSOWTXOAHYJTTDVHAIPVZSZRKTIYSEYIAMKMENCLWCZOJYHZHPUERFZYEMKVMOGRZSTCSDFNNWFSSZSDXTJAVYOWSUNVDBRYIJBETTNQZJNXSRSDRWKMOPHDZCCGKWOIUVWEQWUJNXSFKAGWEPBZHNJEIGFREJBVNNHMYTUNSYTLYOEITCSPTUIUDFNDGCJSDKZQLICKJNOSIYADBFWCJCGJRVHVBIOVRSYAIIYHZFZSVZGKNGVHZTNNWYFVZOCWEVRPJXKFVXSZRDDCJBJYEMBRYIJBRYTCSGWONDVHTJTRXCVBUFLYSIFIGWELMTQRRPVWXSFJFJYAOSXTVZFETRVBUNTCCLLHOHYFTTCLZNYSIXTJCUFNYOXWEZRNNTCAVBHTMFZWJICIWVBKYOMSFUEIHYJCVGVBHZBZMAQSJTMPQYYOGCJJAIRNJHVJVSOOVZSGOCXFIITITMDHZHAIBFYUIRVWSOOEIIFBFBTCOKRADGZJHVGSJEIDIJSNWELFJFWZROVVWIIJVXTDURYIJBRSDDHZXCGSRWTCOKXHZKRXDZSGQYYWJYRZGJJDWMKMERVFQEDBTNDZBKXHZZFAENHYJLDPIFRTOEIWJICIDJOEDTCWELTJDITTZQKNTCCNJVZFJMEDGDJRZZPFSZFMFNOCWYHZSJYAOSRSDNIIJLTAPXTVHLXANDIJSZBKTWISILIQSJLRZOKJRRSZLHOHFRYQWVBSVBUBINVVXWCWCJINZVXCGSRWLTHIJSKOJXEYVVXEZAJSOOHFMAQSTFUNSUFNTRRRABSRSDZJVSIAVVBANWEYEIRZSGOCJYEVZWWOHAVMINIEYIHSCDDZOKMFJFVXTVZCJDOVRYPGOEMECOJFLMSRIYKOZITCSGWIXSWTRCWJRINRVJDNOEIIYCETTNSVFNTFVFSJBKTCJBKNNPSKTPJYVFNYDITBZOKBHVHDZSOGLWEGMSJAMCLYIISTFSZWDZSOWEXINHKMAOMFZBMWELAAWEFLCOCYTJMFZRDBMJSOWXFTDCEXAIRCJTCWDWENHZSPZOTJLZHLXNJHZSVDHVLONGZUAOHYNSXFZYIXOCYIHSPTUMGZSFMWVSDNVZURJUVWS"


def hillclimb_crack(ciphertext):
    period = find_key_size(ciphertext)

    key = ['A']*period

    fit = -100
    while fit < -10:
        print("Current key: {}, fit: {}".format("".join(key), fit))
        working_key = key[:]
        variant_index = random.randint(0, period - 1)
        for c in string.ascii_uppercase:
            working_key[variant_index] = c
            plaintext = decrypt(ciphertext, "".join(working_key))
            test_fit = fitness(plaintext)
            if test_fit > fit:
                key = working_key[:]
                fit = test_fit
    print("Final key: {}, fit: {}".format("".join(key), fit))
    return "".join(key)
    
def main():
    key = hillclimb_crack(real_text) 
    decrypted_text = decrypt(real_text, key)
    print(decrypted_text)


def example_encrypt():
    encrypted_text = encrypt(example_text, key)
    print(encrypted_text)
    decrypted_text = decrypt(encrypted_text, key)
    print(decrypted_text)



if __name__ == "__main__":
    main()

