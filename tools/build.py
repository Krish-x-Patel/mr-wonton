#!/usr/bin/env python3
"""Builds index.html for Mr. Wonton from one menu list, so prices only live in one place.

Prices come from Mr. Wonton's own online ordering page (mrwontononline.com), copied Nov 22, 2026.
A price ending in "+" means the dish comes in more than one size and the price shown is the smallest.
"""
import html

ORDER = "https://www.mrwontononline.com/"
MAPS = "https://www.google.com/maps/dir/?api=1&destination=3595+Canton+Rd+Ste+328+Marietta+GA+30066"
EMBED = "https://www.google.com/maps?q=3595+Canton+Rd+Ste+328,+Marietta,+GA+30066&output=embed"
TEL = "tel:+17705914288"

# group id, group title, note, items: (name, price, description)
MENU = [
 ("specials", "Day specials for one", "Served all day with vegetable fried rice and an egg roll. Swap the egg roll for egg drop, hot and sour or wonton soup for 50¢. Chicken or beef fried rice is $2 more; shrimp or house special fried rice, or lo mein, is $2 more.", [
  ("Chicken with broccoli", "11.55", ""),
  ("Beef with broccoli", "11.55", ""),
  ("Chicken with garlic sauce", "11.55", ""),
  ("Beef with garlic sauce", "11.55", ""),
  ("Kung pao chicken with peanuts", "11.55", ""),
  ("General Tso's chicken", "11.95", ""),
  ("Black pepper chicken", "11.95", ""),
  ("Sesame chicken", "11.95", ""),
  ("Sweet and sour chicken", "11.55", ""),
  ("Sweet and sour pork", "11.55", ""),
  ("Moo goo gai pan", "11.55", ""),
  ("Pork egg foo young", "11.55", ""),
  ("Chicken egg foo young", "11.55", ""),
  ("Boneless spare ribs", "11.95", ""),
  ("Fried chicken wings (8)", "11.55", ""),
  ("Spicy garlic wings (8)", "11.95", ""),
  ("Hot wings (8)", "11.95", ""),
  ("General Tso's wings (8)", "11.95", ""),
  ("Lemon wings (8)", "11.95", ""),
  ("Pepper steak with onion", "11.55", ""),
  ("Chicken with mixed vegetables", "11.55", ""),
  ("Chicken with cashew nuts", "11.55", ""),
  ("Pork lo mein", "11.55", ""),
  ("Chicken lo mein", "11.55", ""),
  ("Beef with mixed vegetables", "11.55", ""),
  ("Mongolian beef", "11.55", ""),
  ("Shrimp with lobster sauce", "11.95", ""),
  ("Spicy garlic shrimp", "11.95", ""),
  ("Shrimp with broccoli", "11.95", ""),
  ("Szechuan shrimp", "11.95", ""),
 ]),
 ("appetizers", "Appetizers", "", [
  ("Pork egg roll (each)", "1.59", ""),
  ("Shrimp roll (each)", "1.59", ""),
  ("Vegetable spring roll (each)", "1.59", ""),
  ("Crab rangoon (5)", "4.25", "Cream cheese filling"),
  ("Crab rangoon (10)", "6.95", "Cream cheese filling"),
  ("Fried wontons (10)", "6.25", "Meat filling"),
  ("Steamed pot stickers", "6.95", ""),
  ("Fried pot stickers", "6.95", ""),
  ("Teriyaki chicken on a stick (4)", "6.95", ""),
  ("Bone-in barbecue ribs (5)", "10.95", ""),
  ("Bone-in barbecue ribs (10)", "20.50", ""),
  ("Boneless spare ribs, small", "8.75", ""),
  ("Boneless spare ribs, large", "16.25", ""),
  ("Fried scallops (12)", "6.50", ""),
  ("Fried shrimp (12)", "6.50", ""),
  ("Shrimp toast (6)", "6.95", ""),
  ("Fried chicken wings (8)", "8.25", ""),
  ("Spicy garlic chicken wings (8)", "8.75", ""),
  ("General Tso's chicken wings (8)", "8.75", ""),
  ("Hot wings (8)", "8.75", ""),
  ("Lemon pepper wings (8)", "8.75", ""),
  ("Sesame balls (6)", "4.95", ""),
  ("French fries, large", "4.25", ""),
 ]),
 ("soup", "Soup", "Served with fried noodle chips.", [
  ("Wonton soup", "2.75+", ""),
  ("Egg drop soup", "2.75+", ""),
  ("Chicken noodle soup", "2.75+", ""),
  ("Chicken rice soup", "2.75+", ""),
  ("Wonton egg drop mix", "2.95+", ""),
  ("Hot and sour soup", "2.95+", ""),
  ("Tofu vegetable soup", "5.50", ""),
  ("Chicken with creamy corn soup", "6.50", ""),
  ("House special soup", "6.95", "Shrimp, chicken and pork with vegetables"),
  ("Seafood vegetable soup", "7.50", "Shrimp, scallops, crabmeat and crawfish with vegetables"),
 ]),
 ("lo-mein", "Lo mein", "Soft Chinese noodles.", [
  ("Vegetable lo mein", "6.95+", ""),
  ("Roast pork lo mein", "7.25+", ""),
  ("Chicken lo mein", "7.25+", ""),
  ("Beef lo mein", "7.75+", ""),
  ("Shrimp lo mein", "7.75+", ""),
  ("House special lo mein", "7.95+", "Chicken, pork and shrimp"),
  ("Seafood lo mein", "8.25+", ""),
 ]),
 ("mai-fun", "Mai fun", "Thin rice noodles. Large size.", [
  ("Fresh vegetable mai fun", "11.25", ""),
  ("Roast pork mai fun", "11.55", ""),
  ("Chicken mai fun", "11.55", ""),
  ("Beef mai fun", "11.95", ""),
  ("Shrimp mai fun", "11.95", ""),
  ("House mai fun", "12.25", ""),
  ("Singapore mai fun", "12.50", "Chicken, pork and shrimp sauteed with curry powder"),
  ("Seafood mai fun", "12.95", "Shrimp, crabmeat and crawfish"),
 ]),
 ("fried-rice", "Fried rice", "", [
  ("Vegetable fried rice", "6.75+", ""),
  ("Roast pork fried rice", "6.95+", ""),
  ("Chicken fried rice", "6.95+", ""),
  ("Beef fried rice", "7.25+", ""),
  ("Shrimp fried rice", "7.25+", ""),
  ("House special fried rice", "7.50+", "Chicken, pork and shrimp"),
  ("Seafood fried rice", "7.75+", ""),
 ]),
 ("egg-foo-young", "Egg foo young", "Large size, with white rice.", [
  ("Vegetable egg foo young", "11.25", ""),
  ("Roast pork egg foo young", "11.75", ""),
  ("Chicken egg foo young", "11.75", ""),
  ("Beef egg foo young", "11.95", ""),
  ("Shrimp egg foo young", "11.95", ""),
  ("House egg foo young", "12.25", ""),
 ]),
 ("vegetable", "Vegetable and tofu", "Large size, with white rice.", [
  ("Vegetable delight", "11.75", ""),
  ("Mixed vegetables with garlic sauce", "11.75", ""),
  ("Sauteed broccoli", "11.75", ""),
  ("Vegetables with fried tofu", "12.25", ""),
  ("Spicy garlic tofu with vegetables", "12.25", ""),
  ("General Tso's tofu with vegetables", "12.25", "Fried tofu and mixed vegetables in a sweet and spicy sauce"),
 ]),
 ("pork-beef", "Pork and beef", "Large size, with white rice.", [
  ("Roast pork with broccoli", "12.95", ""),
  ("Sweet and sour pork", "12.95", ""),
  ("Shredded pork with black bean sauce", "12.95", ""),
  ("Sha cha roast pork", "12.95", ""),
  ("Twice-cooked roast pork", "12.95", ""),
  ("Moo shu pork (5 pancakes)", "12.95", "Pork sauteed with cabbage, mushroom, carrots, bamboo shoots and egg, with plum sauce"),
  ("Beef with broccoli", "13.75", ""),
  ("Pepper steak with onion", "13.75", ""),
  ("Beef with mixed vegetables", "13.75", "Broccoli, carrot, snow peas, baby corn, napa, water chestnuts and mushroom in brown sauce"),
  ("Beef with vegetables in garlic sauce", "13.75", ""),
  ("Szechuan beef", "13.75", ""),
  ("Mongolian beef", "13.75", "Sliced beef sauteed with onions and scallions"),
  ("Hot and spicy beef", "13.75", ""),
 ]),
 ("poultry", "Chicken", "Large size, with white rice.", [
  ("Chicken with broccoli", "12.95", "Sliced white-meat chicken with broccoli in brown sauce"),
  ("Chicken with cashew nuts", "12.95", "Diced chicken with carrot, broccoli stem, baby corn and mushroom in brown sauce, topped with cashews"),
  ("Moo goo gai pan", "12.95", "Sliced white-meat chicken with mushroom, napa, snow peas, carrots and baby corn in white sauce"),
  ("Chicken with black bean sauce", "12.95", "With onions, green pepper, mushroom, baby corn and carrots"),
  ("Chicken with mixed vegetables", "12.95", ""),
  ("Curry chicken with onion", "12.95", "With onion, green pepper, mushroom, baby corn and carrot in curry sauce"),
  ("Kung pao chicken", "12.95", "Diced chicken with carrot, water chestnuts, broccoli stem and green pepper in spicy brown sauce, topped with peanuts"),
  ("Sweet and sour chicken", "12.95", ""),
  ("Sha cha chicken", "12.95", "With vegetables in Chinese barbecue sha cha sauce"),
  ("Fried almond chicken", "12.95", "Battered white-meat chicken topped with almonds, brown gravy on the side"),
  ("Spicy honey chicken with vegetables", "12.95", "Sliced white-meat chicken with mixed vegetables in sweet and spicy sauce"),
  ("Hunan chicken", "12.95", "Spicy white-meat chicken with mixed vegetables"),
  ("Chicken with garlic sauce", "12.95", "With broccoli, mushroom, baby corn, snow peas, water chestnuts, carrot and green pepper"),
  ("Mongolian chicken", "12.95", ""),
  ("Hot and spicy chicken", "12.95", "With shredded carrot, bamboo shoots, snow peas, mushroom and green pepper in spicy brown sauce"),
  ("Moo shu chicken (5 pancakes)", "12.95", ""),
  ("Szechuan chicken", "12.95", ""),
  ("Orange chicken", "13.75", "Battered chicken with orange peel in sweet and spicy sauce"),
  ("General Tso's chicken", "13.75", ""),
  ("Sesame chicken", "13.75", ""),
  ("Teriyaki chicken", "13.75", ""),
  ("Black pepper chicken", "13.75", ""),
 ]),
 ("seafood", "Seafood", "Large size, with white rice.", [
  ("Shrimp with broccoli", "14.25", ""),
  ("Shrimp with lobster sauce", "14.25", ""),
  ("Shrimp with snow peas", "14.25", ""),
  ("Shrimp with mixed vegetables", "14.25", ""),
  ("Curry shrimp with onions", "14.25", ""),
  ("Sweet and sour shrimp", "14.25", ""),
  ("Szechuan shrimp", "14.25", ""),
  ("Shrimp with garlic sauce", "14.25", ""),
  ("Sesame shrimp", "14.25", ""),
  ("Hunan shrimp", "14.25", ""),
  ("Hunan scallops", "14.25", ""),
  ("Spicy garlic scallops with vegetables", "14.25", ""),
 ]),
 ("chefs-special", "Chef's specials", "With white rice or vegetable fried rice.", [
  ("Chicken and shrimp", "14.50", "Sliced chicken and jumbo shrimp with Chinese vegetables in the chef's brown sauce"),
  ("Shrimp and chicken with cashew nuts", "14.50", ""),
  ("Mongolian triple delight", "14.95", ""),
  ("Hunan triple", "14.95", "Chicken, beef and jumbo shrimp with mixed vegetables in hot and spicy sauce"),
  ("Four seasons", "14.95", "Jumbo shrimp, sliced pork, beef and chicken with vegetables in brown sauce"),
  ("Triple garlic delight", "14.95", "Shrimp, chicken and beef with mixed vegetables in garlic sauce"),
  ("Dragon and phoenix", "15.25", "Shrimp and vegetables in savory white sauce on one side, crispy chicken in hot, spicy and sweet sauce on the other"),
  ("Shrimp and scallops", "15.25", "Fresh scallops and shrimp with vegetables in white sauce"),
  ("Happy family", "15.55", "Shrimp, scallops, chicken, beef and pork with vegetables in the chef's special sauce"),
  ("Seafood delight", "15.75", "Jumbo shrimp, crawfish, scallops and crabmeat with fresh vegetables in white sauce"),
 ]),
 ("diet", "Steamed (diet menu)", "No added fat, salt or sugar. Large size, with steamed rice.", [
  ("Steamed broccoli", "11.75", ""),
  ("Steamed mixed vegetables", "11.75", ""),
  ("Steamed chicken with mixed vegetables", "12.95", ""),
  ("Steamed shrimp with mixed vegetables", "14.25", ""),
  ("Steamed gourmet garden", "14.55", "Jumbo shrimp, chicken and beef with mixed vegetables"),
 ]),
 ("sides", "Sides", "", [
  ("Steamed white rice", "1.95+", ""),
  ("Fried noodle chips", "0.75", ""),
  ("Sweet and sour sauce", "0.75", ""),
  ("Brown gravy (8 oz)", "0.75", ""),
  ("Fortune cookies (6)", "0.99", ""),
  ("Fortune cookies (12)", "1.95", ""),
 ]),
]

# Party trays, from Mr. Wonton's own party tray flyer. (title, serves note, [(item, price)])
TRAYS = [
 ("Egg rolls or spring rolls", "Pork egg rolls or vegetable spring rolls", [("10 rolls", "14"), ("20 rolls", "26"), ("30 rolls", "36"), ("40 rolls", "46"), ("50 rolls", "56")]),
 ("Fried chicken wings", "Other flavors $2 more: lemon pepper, spicy garlic, General Tso's or hot", [("40 pieces", "38"), ("50 pieces", "46"), ("60 pieces", "54"), ("70 pieces", "62"), ("80 pieces", "68"), ("100 pieces", "83")]),
 ("Crab rangoon", "", [("40 pieces", "26"), ("50 pieces", "32"), ("60 pieces", "37"), ("70 pieces", "42"), ("80 pieces", "47")]),
 ("Fried rice", "Serves 8 to 10", [("Vegetable", "35"), ("Roast pork or chicken", "36"), ("Beef or shrimp", "39"), ("House special", "40")]),
 ("Lo mein", "Serves 8 to 10", [("Vegetable", "38"), ("Roast pork or chicken", "39"), ("Beef or shrimp", "40"), ("House special", "42")]),
 ("Entrees", "Serves 8 to 10. White rice not included", [("Chicken with broccoli", "44"), ("Chicken with mixed vegetables", "44"), ("Sesame chicken", "46"), ("General Tso's chicken", "46"), ("Beef with broccoli", "46"), ("Mongolian beef", "46"), ("Pepper steak with onion", "46"), ("Spicy garlic shrimp with vegetables", "48"), ("Shrimp with broccoli", "48")]),
]

# Grubhub "Best sellers: most ordered", in its order (checked Nov 22, 2026). (menu group, name, badge, blurb)
POPULAR = [
 ("appetizers", "Crab rangoon (5)", "#1 most ordered", "Crispy wontons with a cream cheese filling"),
 ("specials", "Sesame chicken", "#2 most ordered", "Day special with vegetable fried rice and an egg roll"),
 ("appetizers", "Vegetable spring roll (each)", "#3 most ordered", "Crispy, golden and only $1.59"),
 ("specials", "Sweet and sour chicken", "#4 most ordered", "Day special with vegetable fried rice and an egg roll"),
]

e = html.escape
def slug(s): return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-").replace("--", "-")
ITEMS = {(g[0], i[0]): i for g in MENU for i in g[3]}

def money(p):
    plus = p.endswith("+")
    return f'${p.rstrip("+")}' + ('<abbr class="plus" title="More sizes available; smallest size shown">+</abbr>' if plus else "")

def popular_html():
    out = []
    for gid, name, badge, blurb in POPULAR:
        _, price, _ = ITEMS[(gid, name)]
        out.append(f'''        <a class="pop" href="#item-{gid}-{slug(name)}">
          <span class="pop-rank">{e(badge)}</span>
          <span class="pop-name">{e(name.replace(" (each)", ""))}</span>
          <span class="pop-blurb">{e(blurb)}</span>
          <span class="pop-price">{money(price)}</span>
        </a>''')
    return "\n".join(out)

def menu_html():
    out = []
    for gid, title, note, items in MENU:
        n = f'\n            <p class="gnote">{e(note)}</p>' if note else ''
        wide = ' wide' if len(items) > 20 else ''
        out.append(f'          <div class="group{wide}" id="{gid}">\n            <h3><span>{e(title)}</span></h3>{n}\n            <ul>')
        for name, price, desc in items:
            d = f'<span class="desc">{e(desc)}</span>' if desc else ''
            out.append(f'              <li id="item-{gid}-{slug(name)}"><div class="top"><span class="name">{e(name)}</span><span class="dots" aria-hidden="true"></span><span class="price">{money(price)}</span></div>{d}</li>')
        out.append('            </ul>\n          </div>')
    return "\n".join(out)

def trays_html():
    out = []
    for title, note, rows in TRAYS:
        n = f'<p class="tnote">{e(note)}</p>' if note else ''
        r = "".join(f'<tr><td>{e(a)}</td><td>${b}</td></tr>' for a, b in rows)
        out.append(f'        <div class="slip"><h3>{e(title)}</h3>{n}<table>{r}</table></div>')
    return "\n".join(out)

chips = "\n".join(f'        <a href="#{gid}">{e(t)}</a>' for gid, t, _, _ in MENU)

if __name__ == "__main__":
    TEMPLATE = open('tools/template.html').read()
    page = (TEMPLATE.replace('{{POPULAR}}', popular_html()).replace('{{MENU}}', menu_html()).replace('{{CHIPS}}', chips)
            .replace('{{TRAYS}}', trays_html())
            .replace('{{ORDER}}', ORDER).replace('{{MAPS}}', MAPS).replace('{{EMBED}}', EMBED).replace('{{TEL}}', TEL))
    assert '{{' not in page
    open('index.html', 'w').write(page)
    print('built', len(page), 'bytes;', sum(len(g[3]) for g in MENU), 'menu items;', sum(len(t[2]) for t in TRAYS), 'party tray prices')
