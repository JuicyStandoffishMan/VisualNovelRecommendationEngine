from vnrec import vn

engine = vn()

def print_vns(name, vn_ids):
    print(name + ":")
    print("{")
    ind = 1
    for vn_id in vn_ids:
        print("\t" + str(ind) + ". " + engine.get_title(vn_id) + " (" + str(vn_id) + ")")
        ind += 1

    print("}")
    print("")

# Main
while True:
    input_text = input("Enter the VN_ID: ")
    lower = input_text.lower()
    if lower == "" or lower == "exit" or lower == "e" or lower == "quit" or lower == "q":
        break
    vn_id = int(input_text)
    print("Recommendations for " + engine.get_title(vn_id) + ":")

    top_votes = engine.get_user_recommendations(vn_id)
    top_tags = engine.get_tag_recommendations(vn_id)
    top_combined = engine.get_combined_recommendations(vn_id)

    print_vns("Votes (" + str(engine.vote_weight) + ")", top_votes)
    print_vns("Tags (" + str(engine.tag_weight) + ")", top_tags)
    print_vns("Combined", top_combined)
