import sys
import hashlib
import re
from typing import Dict, List, Set, BinaryIO


b2u_maps = {
    "|": "।", "Ô": "‘", "Õ": "’", "Ò": "“", "Ó": "”", "ª¨": "্র্য", "¤cÖ": "ম্প্র", "i¨": "র‌্য", "²": "ক্ষ্ম",
    "°": "ক্ক", "±": "ক্ট", "³": "ক্ত", "K¡": "ক্ব", "¯Œ": "স্ক্র", "µ": "ক্র", "K¬": "ক্ল", "¶": "ক্ষ", "·": "ক্স",
    "¸": "গু", "»": "গ্ধ", "Mœ": "গ্ন", "M¥": "গ্ম", "M­": "গ্ল", "Mªy": "গ্রু", "¼": "ঙ্ক", "•¶": "ঙ্ক্ষ", "•L": "ঙ্খ",
    "½": "ঙ্গ", "•N": "ঙ্ঘ", "”Q¡": "চ্ছ্ব", "”P": "চ্চ", "”Q": "চ্ছ", "”T": "চ্ঞ", "¾¡": "জ্জ্ব", "¾": "জ্জ", "À": "জ্ঝ",
    "Á": "জ্ঞ", "R¡": "জ্ব", "Â": "ঞ্চ", "Ã": "ঞ্ছ", "Ä": "ঞ্জ", "Å": "ঞ্ঝ", "Æ": "ট্ট", "U¡": "ট্ব", "U¥": "ট্ম", "Ç": "ড্ড",
    "È": "ণ্ট", "É": "ণ্ঠ", "Ý": "ন্স", "Ê": "ণ্ড", "š‘": "ন্তু", "Y^": "ণ্ব", "Ë¡": "ত্ত্ব", "Ë": "ত্ত", "Ì": "ত্থ", "Zœ": "ত্ন",
    "Z¥": "ত্ম", "š—¡": "ন্ত্ব", "Z¡": "ত্ব", "_¡": "থ্ব", "˜M": "দ্গ", "˜N": "দ্ঘ", "Ï": "দ্দ", "×": "দ্ধ", "Ø": "দ্ব",
    "™¢": "দ্ভ", "Ù": "দ্ম", "`ª“": "দ্রু", "aŸ": "ধ্ব", "a¥": "ধ্ম", "›U": "ন্ট", "Ú": "ন্ঠ", "Û": "ন্ড", "š¿": "ন্ত্র",
    "š—": "ন্ত", "¯¿": "স্ত্র", "Î": "ত্র", "š’": "ন্থ", "›`": "ন্দ", "›Ø": "ন্দ্ব", "Ü": "ন্ধ", "bœ": "ন্ন", "š^": "ন্ব",
    "b¥": "ন্ম", "Þ": "প্ট", "ß": "প্ত", "cœ": "প্ন", "à": "প্প", "c­": "প্ল", "á": "প্স", "d¬": "ফ্ল", "â": "ব্জ", "ã": "ব্দ",
    "ä": "ব্ধ", "eŸ": "ব্ব", "e­": "ব্ল", "å": "ভ্র", "gœ": "ম্ন", "¤ú": "ম্প", "ç": "ম্ফ", "¤^": "ম্ব", "¤¢": "ম্ভ", "¤£": "ম্ভ্র",
    "¤§": "ম্ম", "¤­": "ম্ল", "«": "্র", "i“": "রু", "iƒ": "রূ", "é": "ল্ক", "ê": "ল্গ", "ë": "ল্ট", "ì": "ল্ড", "í": "ল্প",
    "î": "ল্ফ", "j¦": "ল্ব", "j¥": "ল্ম", "j­": "ল্ল", "ï": "শু", "ð": "শ্চ", "kœ": "শ্ন", "k¦": "শ্ব", "k¥": "শ্ম",
    "k­": "শ্ল", "®‹": "ষ্ক", "®Œ": "ষ্ক্র", "ó": "ষ্ট", "ô": "ষ্ঠ", "ò": "ষ্ণ", "®ú": "ষ্প", "õ": "ষ্ফ", "®§": "ষ্ম", "¯‹": "স্ক",
    "÷": "স্ট", "ö": "স্খ", "¯—": "স্ত", "¯‘": "স্তু", "¯’": "স্থ", "mœ": "স্ন", "¯ú": "স্প", "ù": "স্ফ", "¯^": "স্ব",
    "¯§": "স্ম", "¯­": "স্ল", "û": "হু", "nè": "হ্ণ", "nŸ": "হ্ব", "ý": "হ্ন", "þ": "হ্ম", "n¬": "হ্ল", "ü": "হৃ", "©": "র্",
    "¨": "্য", "&": "্", "Av": "আ", "A": "অ", "B": "ই", "C": "ঈ", "D": "উ", "E": "ঊ", "F": "ঋ", "G": "এ",
    "H": "ঐ", "I": "ও", "J": "ঔ", "K": "ক", "L": "খ", "M": "গ", "N": "ঘ", "O": "ঙ", "P": "চ", "Q": "ছ",
    "R": "জ", "S": "ঝ", "T": "ঞ", "U": "ট", "V": "ঠ", "W": "ড", "X": "ঢ", "Y": "ণ", "Z": "ত", "_": "থ",
    "`": "দ", "a": "ধ", "b": "ন", "c": "প", "d": "ফ", "e": "ব", "f": "ভ", "g": "ম", "h": "য", "i": "র",
    "j": "ল", "k": "শ", "l": "ষ", "m": "স", "n": "হ", "o": "ড়", "p": "ঢ়", "q": "য়", "r": "ৎ", "0": "০",
    "1": "১", "2": "২", "3": "৩", "4": "৪", "5": "৫", "6": "৬", "7": "৭", "8": "৮", "9": "৯", "v": "া",
    "w": "ি", "x": "ী", "y": "ু", "~": "ূ", "…": "ৃ", "‡": "ে", "‰": "ৈ", "Š": "ৗ", "s": "ং", "t": "ঃ",
    "u": "ঁ", "Ö": "্র", "ª" : "্র", "†":"ে", "„": "ৃ", "¯Í": "স্ত", "ˆ": "ৈ", "ÿ" : "ক্ষ","•" : "ক্স","Y\^" : "ণ্ব",
    "˜¡" : "দ্ব","šÍ" : "ন্ত","š\^" : "ন্ব","cø" : "প্ল","¤\^" : "ম্ব","iæ" : "রু","jø" : "ল্ল","kø" : "শ্ল","¯\^" : "স্ব",
    "z" : "ু"
}

u2b_maps = {
    "।": "|", "‘": "Ô", "’": "Õ", "“": "Ò", "”": "Ó", "্র্য": "ª¨", "ম্প্র": "¤cÖ", "র‌্য": "i¨", "ক্ষ্ম": "²", "ক্ক": "°",
    "ক্ট": "±", "ক্ত": "³", "ক্ব": "K¡", "স্ক্র": "¯Œ", "ক্র": "µ", "ক্ল": "K¬", "ক্ষ": "¶", "ক্স": "·", "গু": "¸", "গ্ধ": "»",
    "গ্ন": "Mœ", "গ্ম": "M¥", "গ্ল": "M­", "গ্রু": "Mªy", "ঙ্ক": "¼", "ঙ্ক্ষ": "•¶", "ঙ্খ": "•L", "ঙ্গ": "½", "ঙ্ঘ": "•N",
    "চ্ছ্ব": "”Q¡", "চ্চ": "”P", "চ্ছ": "”Q", "চ্ঞ": "”T", "জ্জ্ব": "¾¡", "জ্জ": "¾", "জ্ঝ": "À", "জ্ঞ": "Á", "জ্ব": "R¡",
    "ঞ্চ": "Â", "ঞ্ছ": "Ã", "ঞ্জ": "Ä", "ঞ্ঝ": "Å", "ট্ট": "Æ", "ট্ব": "U¡", "ট্ম": "U¥", "ড্ড": "Ç", "ণ্ট": "È", "ণ্ঠ": "É", "ন্স": "Ý",
    "ণ্ড": "Ê", "ন্তু": "š‘", "ণ্ব": "Y^", "ত্ত্ব": "Ë¡", "ত্ত": "Ë", "ত্থ": "Ì", "ত্ন": "Zœ", "ত্ম": "Z¥", "ন্ত্ব": "š—¡", "ত্ব": "Z¡",
    "থ্ব": "_¡", "দ্গ": "˜M", "দ্ঘ": "˜N", "দ্দ": "Ï", "দ্ধ": "×", "দ্ব": "Ø", "দ্ভ": "™¢", "দ্ম": "Ù", "দ্রু": "`ª“", "ধ্ব": "aŸ",
    "ধ্ম": "a¥", "ন্ট": "›U", "ন্ঠ": "Ú", "ন্ড": "Û", "ন্ত্র": "š¿", "ন্ত": "š—", "স্ত্র": "¯¿", "ত্র": "Î", "ন্থ": "š’", "ন্দ": "›`",
    "ন্দ্ব": "›Ø", "ন্ধ": "Ü", "ন্ন": "bœ", "ন্ব": "š^", "ন্ম": "b¥", "প্ট": "Þ", "প্ত": "ß", "প্ন": "cœ", "প্প": "à", "প্ল": "c­",
    "প্স": "á", "ফ্ল": "d¬", "ব্জ": "â", "ব্দ": "ã", "ব্ধ": "ä", "ব্ব": "eŸ", "ব্ল": "e­", "ভ্র": "å", "ম্ন": "gœ", "ম্প": "¤ú",
    "ম্ফ": "ç", "ম্ব": "¤^", "ম্ভ": "¤¢", "ম্ভ্র": "¤£", "ম্ম": "¤§", "ম্ল": "¤­", "্র": "«", "রু": "i“", "রূ": "iƒ", "ল্ক": "é",
    "ল্গ": "ê", "ল্ট": "ë", "ল্ড": "ì", "ল্প": "í", "ল্ফ": "î", "ল্ব": "j¦", "ল্ম": "j¥", "ল্ল": "j­", "শু": "ï", "শ্চ": "ð",
    "শ্ন": "kœ", "শ্ব": "k¦", "শ্ম": "k¥", "শ্ল": "k­", "ষ্ক": "®‹", "ষ্ক্র": "®Œ", "ষ্ট": "ó", "ষ্ঠ": "ô", "ষ্ণ": "ò", "ষ্প": "®ú",
    "ষ্ফ": "õ", "ষ্ম": "®§", "স্ক": "¯‹", "স্ট": "÷", "স্খ": "ö", "স্ত": "¯—", "স্তু": "¯‘", "স্থ": "¯’", "স্ন": "mœ", "স্প": "¯ú",
    "স্ফ": "ù", "স্ব": "¯^", "স্ম": "¯§", "স্ল": "¯­", "হু": "û", "হ্ণ": "nè", "হ্ব": "nŸ", "হ্ন": "ý", "হ্ম": "þ", "হ্ল": "n¬",
    "হৃ": "ü", "র্": "©", "্য": "¨", "্": "&", "আ": "Av", "অ": "A", "ই": "B", "ঈ": "C", "উ": "D", "ঊ": "E",
    "ঋ": "F", "এ": "G", "ঐ": "H", "ও": "I", "ঔ": "J", "ক": "K", "খ": "L", "গ": "M", "ঘ": "N", "ঙ": "O", "চ": "P",
    "ছ": "Q", "জ": "R", "ঝ": "S", "ঞ": "T", "ট": "U", "ঠ": "V", "ড": "W", "ঢ": "X", "ণ": "Y", "ত": "Z", "থ": "_",
    "দ": "`", "ধ": "a", "ন": "b", "প": "c", "ফ": "d", "ব": "e", "ভ": "f", "ম": "g", "য": "h", "র": "i", "ল": "j",
    "শ": "k", "ষ": "l", "স": "m", "হ": "n", "ড়": "o", "ঢ়": "p", "য়": "q", "ৎ": "r", "০": "0", "১": "1", "২": "2",
    "৩": "3", "৪": "4", "৫": "5", "৬": "6", "৭": "7", "৮": "8", "৯": "9", "া": "v", "ি": "w", "ী": "x", "ু": "y",
    "ূ": "~", "ৃ": "…", "ে": "‡", "ৈ": "‰", "ৗ": "Š", "ং": "s", "ঃ": "t", "ঁ": "u"
}


def apply_char_map(text: str, char_map: Dict) -> str:
    to_match = "|".join(char_map.keys())
    text = re.sub(to_match, lambda m: char_map[m.group(0)], text)
    return text


def is_bengali_digit(c: str) -> bool:
    if '০' <= c <= '৯':
        return True
    return False


def is_bengali_pre_kar(c: str) -> bool:
    if c == 'ি' or c == 'ৈ' or c == 'ে':
        return True
    return False


def is_bengali_post_kar(c: str) -> bool:
    if c == 'া' or c == 'ৗ' or c == 'ু' or c == 'ূ' or c == 'ী' or c == 'ৃ':
        return True
    return False


def is_bengali_mid_kar(c: str) -> bool:
    if c == 'ো' or c == 'ৌ':
        return True
    return False


def is_bengali_kar(c: str) -> bool:
    if is_bengali_pre_kar(c) or is_bengali_post_kar(c) or is_bengali_mid_kar(c):
        return True
    return False


def is_bengali_banjon_borno(c: str) -> bool:
    if 'ক' <= c <= 'ন' or 'প' <= c <= 'র' or c == 'ল' or 'শ' <= c <= 'হ' or c == 'ড়' or c == 'ঢ়' or c == 'য়' \
            or c == 'ৎ' or c == 'ং' or c == 'ঃ' or c == 'ঁ':
        return True
    return False


def is_bengali_sor_borno(c: str) -> bool:
    if 'অ' <= c <= 'ঌ' or c == 'এ' or c == 'ঐ' or c == 'ও' or c == 'ঔ':
        return True
    return False


def is_bengali_chandrabindu(c: str) -> bool:
    if c and hex(ord(c)) == '0x981':
        return True
    return False


def is_bengali_hasant(c: str) -> bool:
    if c and hex(ord(c)) == '0x9cd':
        return True
    return False


def is_bengali_nukta(c: str) -> bool:
    if c and hex(ord(c)) == '0x9bc':
        return True
    return False


def is_space(c: str) -> bool:
    if c == ' ' or c == '\t' or c == '\n' or c == '\r':
        return True
    return False


def get_char(a_string: str, place_holder: int) -> str:
    if place_holder < 0 or place_holder >= len(a_string):
        return ""
    return a_string[place_holder]


def _find_hasant_chain(a_string: str, pos: int) -> int:
    if not is_bengali_hasant(get_char(a_string, pos + 2)):
        return pos
    return _find_hasant_chain(a_string, pos + 2)


def _rearrange_groups(groups: List) -> List:
    """
    Re-arrange the groups by having some considerations in mind
    Considerations:
    1. ref + banjonborno -> banjonborno + ref
    2. banjonborno + prekar -> prekar + banjonborno
    3. banjonborno + okar -> ekar + banjonborno + akar
    4. banjonborno + oukar -> ekar + banjonborno + "ৗ"
    """
    for i in range(len(groups)):
        has_postkar = False
        has_midkar = False
        if is_bengali_pre_kar(groups[i][-1][1]):
            # send prekar to the front
            groups[i].insert(0, groups[i].pop())
        elif is_bengali_post_kar(groups[i][-1][1]):
            has_postkar = True
        elif is_bengali_mid_kar(groups[i][-1][1]):
            has_midkar = True
            if groups[i][-1][1] == "ো":
                groups[i].insert(0, (hex(ord("ে")), "ে") )
                groups[i].pop()
                groups[i].insert(len(groups[i]), (hex(ord("া")), "া"))
            elif groups[i][-1][1] == "ৌ":
                groups[i].insert(0, (hex(ord("ে")), "ে"))
                groups[i].pop()
                groups[i].insert(len(groups[i]), (hex(ord("ৗ")), "ৗ"))
        hasant_ind = _get_hasant_indices(groups[i])
        for j in hasant_ind:
            if groups[i][j-1][1] == 'র':
                # send ref to the last pos if there is no postkar
                # if there is a postKar send it to the 2nd last position
                if has_postkar or has_midkar:                   
                    groups[i].insert(-1, groups[i].pop(j))
                    groups[i].insert(-2, groups[i].pop(j-1))
                else:
                    groups[i].insert(len(groups[i])-1, groups[i].pop(j))
                    groups[i].insert(len(groups[i])-2, groups[i].pop(j-1))
    return groups


def _make_groups(a_string: str) -> List:
    """
    Considerations:
    1. banjonborno > banjonborno (no kar)
    2. shorborno > banjonborno  (no kar)
    3. banjonborno > kar
    4. banjonborno > Hasant (End with hasant)
    5. banjonborno > Hasant > banjonborno (normal juktoborno)
    6. banjonborno > Hasant > banjonborno > kar
    7. banjonborno > Hasant > banjonborno > kar > banjonborno
    8. banjonborno > Hasant > banjonborno > ..... > Hasant > banjonborno
    """
    groups = []
    
    place_holder = 0
    for _ in range(len(a_string)):
        queue = []
        char = get_char(a_string, place_holder)
        char_prev = get_char(a_string, place_holder -1)
        char_next = get_char(a_string, place_holder+1)

        if not char:
            break

        if not char_next:
            # Last character of the word
            groups.append([(hex(ord(char)), char)])
            break

        if is_bengali_hasant(char_next):
            # When the next char is hasant, just increase place_holder
            # as the condition for dealing with hasant will also get the banjonborno before it
            place_holder += 1
        
        elif is_bengali_hasant(char):
            # Standing on Hasant
            # append to group as long as there are hasants on 2 places in front
            # means there are multiple Juktoborno0
            temp_placeholder = _find_hasant_chain(a_string, place_holder)
            
            if is_bengali_banjon_borno(char_prev):
                # Get the prev banjonborno i.e. for গর্ব get র or for অন্ত get ন
                queue.append((hex(ord(char_prev)), char_prev))
            
            while place_holder <= temp_placeholder:
                # deal with the hasant chain
                queue.append((hex(ord(get_char(a_string, place_holder))), get_char(a_string, place_holder)))
                place_holder += 1

            if is_bengali_kar(get_char(a_string, place_holder)):
                # banjonborno > Hasant > banjonborno > kar
                queue.append((hex(ord(get_char(a_string, place_holder))), get_char(a_string, place_holder)))
                # place_holder += 1

            elif is_bengali_banjon_borno(get_char(a_string, place_holder)):
                # banjonborno > Hasant > banjonborno > kar
                queue.append((hex(ord(get_char(a_string, place_holder))), get_char(a_string, place_holder)))
                place_holder += 1
            
            if is_bengali_kar(get_char(a_string, place_holder)):
                # banjonborno > Hasant > banjonborno > kar
                queue.append((hex(ord(get_char(a_string, place_holder))), get_char(a_string, place_holder)))
                place_holder += 1
 
            groups.append(queue)

        elif (is_bengali_banjon_borno(char) or is_bengali_sor_borno(char)) and (is_bengali_banjon_borno(char_next) or
                                                                                is_bengali_sor_borno(char_next)):
            # if 2 banjonborno/shorborno are one after another, append the 1st one in groups
            # Example: কলম, আম
            groups.append([(hex(ord(char)), char)])
            place_holder += 1
        
        elif is_bengali_banjon_borno(char) and is_bengali_kar(char_next):
            # if there is kar after a banjonborno, deal with that
            # Example: আসে,বসে,আকাশে,বাতাসে
            queue.append((hex(ord(char)), char))
            queue.append((hex(ord(char_next)), char_next))
            place_holder += 2
            groups.append(queue)
    
    return _rearrange_groups(groups)


def _get_hasant_indices(group):
    """
    Return all the positions that has hasant in the group
    """
    indices = []
    for i, char in enumerate(group):
        if is_bengali_hasant(char[1]):
            indices.append(i)
    return indices


def _shift_right(target: List, pos: int) -> List:
    """
    Shift prekars to right until stopping condition is met
    """   
    #Blind shift once
    target[pos], target[pos+1] = target[pos+1], target[pos]
    pos += 1

    #If there is a ref at the right, shift again
    if pos < len(target)-1:
        if target[pos+1] == "©" or target[pos+1] == "¨" or target[pos+1] == "«" or target[pos+1] == "ª":
            target[pos], target[pos+1] = target[pos+1], target[pos]
    return target


def _rearrange_b2u(target: List, prekar_set: Set) -> List:
    # store the indices of refs, prekars and postkars in these lists
    refs = []
    prekars = []
    chondrobindus = []
    fola_set = {"…", "ª", "«", "¨", "Ö", "„"}
    kar_set = {"‡", "w", "‰", "†", "ˆ","v", "Š", "y", "~", "x", "…" }
    for i, char in enumerate(target):
        if char in prekar_set:
            # if the character I'm standing on is a prekar
            prekars.append(i)
                
    for pr in prekars:
        if target[pr+1] == "©" or target[pr+1] in fola_set:
            target[pr+1], target[pr+2] = target[pr+2], target[pr+1]
        target = _shift_right(target, pr)

    for i, char in enumerate(target):
        if char == "©":
            # if the character I'm standing on is a ref
            refs.append(i)

    for r in refs:
        # rearrange all the refs
        # banjonborno(or juktoborno) + ref => ref + banjonborno(or juktoborno)
        target[r], target[r-1] = target[r-1], target[r]
        if (target[r] in fola_set) or (target[r] in kar_set) :
            target[r-1], target[r-2] = target[r-2], target[r-1]
    
    for i, char in enumerate(target):
        if char == "u":
            # if the character I'm standing on is a chondrobindu
            chondrobindus.append(i)
    
    for c in chondrobindus:
        if target[c+1] in kar_set:
            target[c+1], target[c] = target[c], target[c+1]

    return target
    

def bijoy2unicode(src_string: str) -> str:
    """
    Convert Ansi Bijoy encoded Bengali string to Unicode
    :param src_string:
    :return:
    """
    if not src_string:
        # If there is nothing in input return the same
        return src_string

    prekar_set = {"‡", "w", "‰", "†", "ˆ"}

    escaped_bijoy_chars = (re.escape(a_bijoy) for a_bijoy in b2u_maps.keys())
    to_match = "("+"|".join(escaped_bijoy_chars)+")"
    target = [a_split for a_split in re.split(to_match, src_string) if a_split]
        
    target = _rearrange_b2u(target, prekar_set)
    target_string = ""

    for i, t in enumerate(target):
        if i < len(target)-1:
            if (t in prekar_set) and (target[i+1] == "Š"):
                # ekar + banjonborno (or juktoborno) + akar(with urani)
                # banjonborno (or juktoborno) + oukar
                del target[i]
                target_string += "ৌ"
                continue
            elif t in prekar_set and target[i+1] == "v":
                # ekar + banjonborno (or juktoborno) + akar
                # banjonborno (or juktoborno) + okar
                del target[i]
                target_string += "ো"
                continue

        target_string += b2u_maps.get(t, t)
    return target_string


def unicode2bijoy(src_string: str) -> str:
    """
    Converts a string from unicode format to ANSI Bijoy format
    :param src_string: Source string in unicode
    :return: src_string formatted in Bijoy
    """
    if not src_string:
        # If there is nothing in input return the same
        return src_string

    target_string = ""
    groups = _make_groups(src_string)

    for group in groups:
        temp_string = ""
        for char in group:
            # append the characters in a string
            temp_string += char[1]
        target_string += apply_char_map(temp_string, u2b_maps)
    return target_string


def file_hash(f_in: BinaryIO, buffer_size = 65536) -> str:
    """
    Given a file stream opened in binary mode, constructs a MD5 hash for the file
    """
    md5 = hashlib.md5()
    while True:
        data = f_in.read(buffer_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

