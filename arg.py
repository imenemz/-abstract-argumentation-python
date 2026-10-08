def read_graph(text):
    arguments = []
    attacks = []

    for line in text.replace('\n', ' ').split('.'):
        line = line.strip()

        if line.startswith('arg('):
            name = line[4:-1].strip()
            arguments.append(name)

        elif line.startswith('att('):
            inside = line[4:-1]
            a, b = inside.split(',')
            attacks.append((a.strip(), b.strip()))

    # Remove self-attacking arguments
    self_attackers = []

    for (a, b) in attacks:
        if a == b:
            self_attackers.append(a)

    # Remove self-attacking arguments
    arguments = [arg for arg in arguments if arg not in self_attackers]

    # Remove all attacks involving them
    attacks = [
        (a, b) for (a, b) in attacks
        if a not in self_attackers and b not in self_attackers
    ]

    return arguments, attacks


#Part 2 : Generate all possible subsets


def all_subsets(lst):
    # Base case : if the list is empty, the only subset is {}
    if len(lst) == 0:
        return [[]]

    # Take the first element
    first = lst[0]
    rest = lst[1:]

    # Get all subsets of the rest (without first element)
    subsets_without_first = all_subsets(rest)

    # Add first element to each of those subsets
    subsets_with_first = []
    for s in subsets_without_first:
        subsets_with_first.append([first] + s)

    # Return both : subsets with and without first
    return subsets_without_first + subsets_with_first


#Part 3 : Check the properties of a set S

def get_attackers(arg, attacks):
    # Returns all arguments that attack 'arg'
    result = []
    for (a, b) in attacks:
        if b == arg:
            result.append(a)
    return result

def attacked_by(S, attacks):
    # Returns all arguments attacked by at least one member of S
    result = []
    for (a, b) in attacks:
        if a in S:
            result.append(b)
    return result

def is_conflict_free(S, attacks):
    # S is conflict-free if no member of S attacks another member of S
    # Example : if a attacks b, then {a, b} is NOT conflict-free
    for (a, b) in attacks:
        if a in S and b in S:
            return False   # found a conflict -> not ok
    return True            # no conflict found -> ok

def is_admissible(S, attacks):
    # S is admissible if :
    # 1. S is conflict-free
    # 2. S defends all its members
    #    (every attacker of a member of S is itself attacked by S)

    # Check condition 1
    if not is_conflict_free(S, attacks):
        return False

    # Check condition 2
    targets_of_S = attacked_by(S, attacks)  # who does S attack ?
    for arg in S:
        for attacker in get_attackers(arg, attacks):
            if attacker not in targets_of_S:
                return False   # S does not defend 'arg' -> not admissible
    return True

def is_complete(S, arguments, attacks):
    # S is complete if :
    # 1. S is admissible
    # 2. S contains ALL arguments it defends
    #    (if S defends an argument outside of S, it's not complete)

    # Check condition 1
    if not is_admissible(S, attacks):
        return False

    # Check condition 2
    targets_of_S = attacked_by(S, attacks)
    for arg in arguments:
        if arg not in S:
            # Does S defend this argument ?
            all_attackers = get_attackers(arg, attacks)
            S_defends_it = all(att in targets_of_S for att in all_attackers)
            if S_defends_it:
                return False   # S defends arg but arg is not in S -> not complete

    return True


# Part4 : The three semantics
#c est un ensemble adminsible qui contient tous les aurg qui est capable de les defendre 
def complete_extensions(arguments, attacks):
    # Returns all subsets that are complete
    extensions = []
    for S in all_subsets(arguments):
        if is_complete(S, arguments, attacks):
            extensions.append(S)
    return extensions
#c'est la position la plus prutent est unique contient les args sur 
def grounded_extension(arguments, attacks):
    # The grounded extension = the SMALLEST complete extension
    # intersection of all complete extensions
    # It is the most cautious semantics : only accept what we are sure about

    all_complete = complete_extensions(arguments, attacks)
    if not all_complete:
        return []

    # Start with the first complete extension
    result = all_complete[0][:]

    # Keep only arguments that appear in ALL extensions
    for ext in all_complete[1:]:
        result = [arg for arg in result if arg in ext]

    return result
#cherche a former le plus grand groupe choerent possiblle 
def preferred_extensions(arguments, attacks):
    # The preferred extensions = the LARGEST complete extensions
    # = complete extensions that are not contained in any other complete extension
    # It is the most bold semantics : accept as much as possible

    all_complete = complete_extensions(arguments, attacks)
    preferred = []

    for ext in all_complete:
        is_maximal = True
        for other in all_complete:
            if ext != other:
                # Is 'ext' strictly contained in 'other' ?
                ext_inside_other = all(arg in other for arg in ext)
                if ext_inside_other and len(other) > len(ext):
                    is_maximal = False
                    break
        if is_maximal:
            preferred.append(ext)

    return preferred


#Part 5 : display and run

def show(S):
    # Pretty print a set of arguments
    if len(S) == 0:
        return "{}"
    return "{" + ", ".join(sorted(S)) + "}"

def run(input_text):
    print("=" * 50)
    print("INPUT :")
    print(input_text.strip())
    print("=" * 50)

    arguments, attacks = read_graph(input_text)

    print(f"\nArguments : {arguments}")
    print(f"Attacks   : {attacks}\n")

    co = complete_extensions(arguments, attacks)
    gr = grounded_extension(arguments, attacks)
    pr = preferred_extensions(arguments, attacks)

    print("CO extensions (complete) :")
    for ext in co:
        print("   ", show(ext))

    print("\nGR extension (grounded) :")
    print("   ", show(gr))

    print("\nPR extensions (preferred) :")
    for ext in pr:
        print("   ", show(ext))

    print("=" * 50)


#testing

if __name__ == "__main__":

    print("\n test 1 : Chain a -> b -> c \n")
    run("""
    arg(a).
    arg(b).
    arg(c).
    att(a,b).
    att(b,c).
    """)

    print("\n Test 2 : Nixon Diamond a <-> b\n")
    run("""
    arg(a).
    arg(b).
    att(a,b).
    att(b,a).
    """)

    print("\n Test 3 : Nixon Diamond + node c\n")
    run("""
    arg(a).
    arg(b).
    arg(c).
    att(a,b).
    att(b,a).
    att(b,c).
    """)

    print("\n Test 4 : Odd cycle a -> b -> c -> a\n")
    run("""
    arg(a).
    arg(b).
    arg(c).
    att(a,b).
    att(b,c).
    att(c,a).
    """)

    print("\n Test 5: a -> b, a -> c, b -> d, c -> d\n")
    run("""
    arg(a).
    arg(b).
    arg(c).
    arg(d).
    att(a,b).
    att(a,c).
    att(b,d).
    att(c,d).
    """)

    print("\n Test\n")
    run("""
    arg(a).
    arg(b).
    att(a,b).
    att(a,a).
   
    """)