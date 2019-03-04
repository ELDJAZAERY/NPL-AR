# -*- coding: utf-8 -*-

# H I S T O R I C A L
# D I C T I O N A R Y


from   lxml import etree



# DICTIONARY STRUCTURE
"""
dictionary = {
     'word': (
             True,                                  # is_valid      0
             {                                      # eras          1
                'era1': ('def1', ['e1', 'e2']),
                'era2': ('def2', ['e1', 'e2'])
             }
            )
}
"""

# XML STRUCTURE
"""
<?xml version="1.0" encoding="UTF-8"?>
<entries>
  <entry name='word'>
    <era name='era name'>
      <def>
        definition
      </def>
      <examples>
        <example>example 1</example>
        <example>example 2</example>
      </examples>
    </era>
  </entry>
</entries>
"""

# CREATE A DICTIONARY FORM FILE
# Set is_valid to False when loading the non valid dictionary
def load_dict(filename, is_valid=True):
    hist_dict = {}
    
    try:
        tree = etree.parse(filename)
        for entry in tree.xpath('/entries/entry'):
            word = entry.get('name')
            eras = {}
            for era in entry.getchildren():                       # <era> in <entry> tag
                era_name = era.get('name')
                word_def = era.getchildren()[0].text.strip()      # <def> in <era> tag
                examples_list = []
                for ex in era.getchildren()[1]:                   # <example> in <era> tag
                    examples_list.append(ex.text.strip())
                eras[era_name] = (word_def, examples_list)
            hist_dict[word] = (is_valid, eras)
    except: print('### Dict Vide ###'); pass
    return hist_dict


# print(load_dict('dicts/hist_dict.xml'))
# print(load_dict('dicts/hist_dict_not_valid.xml'))


# CEARTE AN XML FILE FOR THE DICTIONARY
# Set is_valid to False to save the non valid enteries of the dictionary
def save_dict(hist_dict, filename, is_valid=True):
    entries = etree.Element('entries')
    for w in sorted(hist_dict.keys()):
        if (hist_dict[w][0] != is_valid):
            continue
        
        entry    = etree.SubElement(entries, 'entry')
        entry.set('name', w)
        for d_era in hist_dict[w][1]:
            era  = etree.SubElement(entry, 'era')
            era.set('name', d_era)
            word_def = etree.SubElement(era, 'def')
            word_def.text = hist_dict[w][1][d_era][0]
            examples = etree.SubElement(era, 'examples')
            for ex in hist_dict[w][1][d_era][1]:
                example = etree.SubElement(examples, 'example')
                example.text = ex
    
    out = open(filename, 'w')
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.write(etree.tostring(entries, pretty_print=True).__str__())
    out.close



"""
# d = load_dict('dicts/hist_dict.xml')
d = load_dict('dicts/hist_dict_not_valid.xml')
d['another word'] = (False, d['another word'][1])
save_dict(d, 'dicts/new.xml', is_valid=False)
"""



