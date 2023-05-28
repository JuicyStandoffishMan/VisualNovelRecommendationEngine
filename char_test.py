import math
from crec import vnchar
from vnrec import vn

engine = vnchar()
vn = vn(skip_recs=True)

def print_chars(name, cids):
    print(name + ":")
    print("{")
    ind = 1
    for (cid, score) in cids:
        char_name = engine.get_character_name(cid)
        print("\t" + str(ind) + ". " + char_name + " (" + str(cid) + ") with score " + str(round(score * 1000.0) / 1000.0))

        vns = engine.get_char_vns(cid)
        for vid in vns:
            print("\t\t- " + vn.get_title(vid) + " (" + str(vid) + ")")
        
        print("")
        ind += 1

    print("}")
    print("")

# Main
while True:
    input_text = input("Enter the Char ID: ")
    lower = input_text.lower()
    if lower == "" or lower == "exit" or lower == "e" or lower == "quit" or lower == "q":
        break
    cid = int(input_text)
    print("Recommendations for " + engine.get_character_name(cid) + " (" + str(cid) + ")" + f' gender_match={engine.match_gender}, exclude_same_vns={engine.exclude_same_vns}:')

    top_traits = engine.get_trait_recommendations_scores(cid)

    print_chars("Traits", top_traits)
