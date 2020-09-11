# Item url dictionary

# Next Plates to Add:
# https://www.roguefitness.com/rogue-wagon-wheel-pairs

# Next Boneyard Links:
# https://www.roguefitness.com/rogue-socket-pull-up-boneyard-bars
# https://www.roguefitness.com/rogue-mil-echo-bumper-plates-black-closeout
# https://www.roguefitness.com/boneyard-rogue-rackable-curl-bar
# https://www.roguefitness.com/rogue-black-training-lb-color-stripe-plates-closeout
# https://www.roguefitness.com/rogue-mil-echo-bumper-plates-black-closeout?=winNOw

categories = ['acc', 'au', 'barbell', 'bench', 'boneyard', 'cardio', 'cond', 'inf', 'ironmaster', 'm', 'ml',
              'other', 'plate', 'rack', 'spec_bar', 'squat_stand', 'storage', 'uk']


# Return all items from search_urls that match passed in category value
def get_items_by_category(category):
    if category not in categories:
        return []
    else:
        items = []
        for item in search_urls:
            if search_urls[item]['category'] == category:
                items.append(item)
        return items


search_urls = {
    "westside scout hyper": {
        "type": "multi",
        "product_name": "Westside Scout Hyper",
        "link": "https://www.roguefitness.com/westside-scout-hyper",
        "category": "acc",
    },
    "lp-2": {
        "type": "single",
        "product_name": "Rogue LP-2 Lat Pulldown / Low Row",
        "link": "https://www.roguefitness.com/rogue-lp-2-lat-pulldown-low-row",
        "category": "acc",
    },
    "parallel landmine handle": {
        "type": "multi",
        "product_name": "Rogue Parallel Landmine Handle",
        "link": "https://www.roguefitness.com/rogue-parallel-landmine-handle",
        "category": "acc"
    },
    "mini dl jack": {
        "type": "single",
        "product_name": "Mini Deadlift Bar Jack",
        "link": "https://www.roguefitness.com/mini-deadlift-bar-jack",
        "category": "acc"
    },
    "dl jack": {
        "type": "single",
        "product_name": "Rogue Deadlift Bar Jack",
        "link": "https://www.roguefitness.com/bar-jack",
        "category": "acc"
    },
    "trolley lever arm kit": {
        "type": "trolley",
        "product_name": "Rogue LT-1 Trolley and Lever Arm Kit",
        "link": "https://www.roguefitness.com/rogue-lt-1-50-cal-trolley-lever-arms-kit",
        "category": "acc"
    },
    "usa alum collars": {
        "type": "custom2",
        "product_name": "Rogue USA Aluminum Collars",
        "link": "https://www.roguefitness.com/rogue-usa-aluminum-collars",
        "category": "acc"
    },
    "landmine post": {
        "type": "single",
        "product_name": "Post Landmine",
        "link": "https://www.roguefitness.com/post-landmine",
        "category": "acc"
    },
    "ab wheel": {
        "type": "single",
        "product_name": "Ab Wheel",
        "link": "https://www.roguefitness.com/ab-wheel",
        "category": "acc"
    },
    "ss lat bar": {
        "type": "single",
        "product_name": "Rogue Stainless Lat Bar",
        "link": "https://www.roguefitness.com/rogue-stainless-steel-lat-bar",
        "category": "acc"
    },
    "grip triangle": {
        "type": "single",
        "product_name": "Rogue Grip Triangle (Standard Grip)",
        "link": "https://www.roguefitness.com/rogue-grip-triangle-standard-grip",
        "category": "acc"
    },
    "tricep pushdown": {
        "type": "single",
        "product_name": "Rogue Tricep Push Down Attachment",
        "link": "https://www.roguefitness.com/rogue-tricep-pushdown-attachment",
        "category": "acc"
    },
    "t-bar row": {
        "type": "multi",
        "product_name": "Rogue T Bar Row",
        "link": "https://www.roguefitness.com/rogue-t-bar-row",
        "category": "acc"
    },
    "echo gym timer": {
        "type": "multi",
        "product_name": "Rogue Echo Gym Timer",
        "link": "https://www.roguefitness.com/rogue-echo-gym-timer",
        "category": "acc"
    },
    "home timer": {
        "type": "multi",
        "product_name": "Rogue Home Timer",
        "link": "https://www.roguefitness.com/rogue-home-timer",
        "category": "acc"
    },
    "landmine handles": {
        "type": "multi",
        "product_name": "Rogue Landmine Handles",
        "link": "https://www.roguefitness.com/rogue-landmine-handles",
        "category": "acc"
    },
    "loading pin": {
        "type": "multi",
        "product_name": "Rogue Loading Pin",
        "link": "https://www.roguefitness.com/rogue-loading-pin",
        "category": "acc"
    },
    "p-4 pullup": {
        "type": "multi",
        "product_name": "Rogue P-4 Pull-up System",
        "link": "https://www.roguefitness.com/p4-pullup-system",
        "category": "acc"
    },
    "speed bag": {
        "type": "custom2",
        "product_name": "Rogue Rig Mount Speed Bag Platforms",
        "link": "https://www.roguefitness.com/rogue-rig-mount-speed-bag-platforms",
        "category": "acc"
    },
    "squat stand storage pair": {
        "type": "single",
        "product_name": "Rogue Squat Stand Base Storage - Pair",
        "link": "https://www.roguefitness.com/rogue-squat-stand-base-storage-pair",
        "category": "acc"
    },
    "horizontal plate rack": {
        "type": "single",
        "product_name": "Rogue Horizontal Plate Rack 2.0",
        "link": "https://www.roguefitness.com/horizontal-plate-rack-2-0",
        "category": "acc"
    },
    "plate tree york": {
        "type": "single",
        "product_name": "York Olympic A-Frame Plate Tree",
        "link": "https://www.roguefitness.com/york-olympic-a-frame-plate-tree",
        "category": "acc"
    },
    "au bench ab2": {
        "type": "multi",
        "product_name": "AU AB-2 Adjustable Bench",
        "link": "https://www.rogueaustralia.com.au/ab-2-adjustable-bench-au",
        "category": "au"
    },
    "au barbell opb zinc": {
        "type": "single",
        "product_name": "AU Rogue 20KG Ohio Power Bar - Black Zinc",
        "link": "https://www.rogueaustralia.com.au/rogue-20-kg-ohio-power-bar-black-zinc-au",
        "category": "au"
    },
    "au barbell opb ss": {
        "type": "single",
        "product_name": "AU Rogue 20KG Ohio Power Bar - Stainless Steel",
        "link": "https://www.rogueaustralia.com.au/rogue-20-kg-ohio-power-bar-stainless-steel-au",
        "category": "au"
    },
    "au sml-1": {
        "type": "multi",
        "product_name": "AU SML-1 Rogue 70\" Monster Lite Squat Stand",
        "link": "https://www.rogueaustralia.com.au/sml-1-rogue-70-monster-lite-squat-stand-au",
        "category": "au"
    },
    "au ml safety spotter arms": {
        "type": "multi",
        "product_name": "AU SAML-24 Monster Lite Safety Spotter Arms (Pair)",
        "link": "https://www.rogueaustralia.com.au/saml-24-monster-lite-spotter-arms-pair-au",
        "category": "au"
    },
    "au plate cal": {
        "type": "multi",
        "product_name": "AU Rogue Calibrated KG Steel Plates",
        "link": "https://www.rogueaustralia.com.au/rogue-calibrated-kg-steel-plates-au",
        "category": "au"
    },
    "au rml-390f": {
        "type": "multi",
        "product_name": "AU RML-390F Flat Foot Monster Lite Rack",
        "link": "https://www.rogueaustralia.com.au/rml-390f-flat-foot-monster-lite-rack-au",
        "category": "au"
    },
    "au model d rower": {
        "type": "single",
        "product_name": "AU Black Concept 2 Model D Rower - PM5",
        "link": "https://www.rogueaustralia.com.au/black-concept-2-model-d-rower-pm5-au",
        "category": "au"
    },
    "barbell freedom 25mm": {
        "type": "single",
        "product_name": "Rogue 25MM Freedom Bar",
        "link": "https://www.roguefitness.com/rogue-25-mm-freedom-bar",
        "category": "barbell",
    },
    "barbell t-15": {
        "type": "single",
        "product_name": "Rogue T-15LB Technique Bar",
        "link": "https://www.roguefitness.com/rogue-t-15-lb-technique-bar",
        "category": "barbell",
    },
    "barbell op oxide": {
        "type": "single",
        "product_name": "The Ohio Bar - Black Oxide",
        "link": "https://www.roguefitness.com/rogue-ohio-bar-black-oxide",
        "category": "barbell"
    },
    "barbell op zinc": {
        "type": "single",
        "product_name": "The Ohio Bar - Black Zinc",
        "link": "https://www.roguefitness.com/the-ohio-bar-black-zinc",
        "category": "barbell"
    },
    "barbell op ecoat": {
        "type": "single",
        "product_name": "The Ohio Bar - E-Coat",
        "link": "https://www.roguefitness.com/the-ohio-bar-2-0-e-coat",
        "category": "barbell"
    },
    "barbell op ss": {
        "type": "single",
        "product_name": "The Ohio Bar - Stainless Steel",
        "link": "https://www.roguefitness.com/stainless-steel-ohio-bar",
        "category": "barbell"
    },
    "barbell op cerakote": {
        "type": "cerakote",
        "product_name": "The Ohio Bar - Cerakote",
        "link": "https://www.roguefitness.com/the-ohio-bar-cerakote",
        "category": "barbell"
    },
    "barbell op fraser": {
        "type": "multi",
        "product_name": "Rogue Athlete Cerakote Ohio Bar - Fraser Edition",
        "link": "https://www.roguefitness.com/rogue-athlete-ohio-bar-fraser-cerakote-edition",
        "category": "barbell"
    },
    "barbell opb steel": {
        "type": "single",
        "product_name": "Rogue 45LB Ohio Power Bar - Bare Steel",
        "link": "https://www.roguefitness.com/rogue-45lb-ohio-power-bar-bare-steel",
        "category": "barbell"
    },
    "barbell opb ecoat": {
        "type": "single",
        "product_name": "Rogue 45LB Ohio Power Bar - E-Coat",
        "link": "https://www.roguefitness.com/rogue-ohio-power-bar-e-coat",
        "category": "barbell"
    },
    "barbell opb zinc": {
        "type": "single",
        "product_name": "Rogue 45LB Ohio Power Bar - Black Zinc",
        "link": "https://www.roguefitness.com/rogue-45lb-ohio-power-bar-black-zinc",
        "category": "barbell"
    },
    "barbell opb ss": {
        "type": "custom",
        "product_name": "Rogue 45LB Ohio Power Bar - Stainless Steel",
        "link": "https://www.roguefitness.com/rogue-45lb-ohio-power-bar-stainless",
        "category": "barbell"
    },
    "barbell opb ss kg": {
        "type": "single",
        "product_name": "Rogue 20KG Ohio Power Bar - Stainless Steel",
        "link": "https://www.roguefitness.com/rogue-20-kg-ohio-power-bar-stainless-steel",
        "category": "barbell"
    },
    "barbell opb cerakote": {
        "type": "cerakote",
        "product_name": "Rogue 45LB Ohio Power Bar - Cerakote",
        "link": "https://www.roguefitness.com/rogue-45lb-ohio-powerlift-bar-cerakote",
        "category": "barbell"
    },
    "barbell dl cerakote": {
        "type": "cerakote",
        "product_name": "Rogue Ohio Deadlift Bar - Cerakote",
        "link": "https://www.roguefitness.com/rogue-ohio-deadlift-cerakote",
        "category": "barbell"
    },
    "bella ecoat": {
        "type": "single",
        "product_name": "The Bella Bar 2.0 - E-Coat",
        "link": "https://www.roguefitness.com/the-bella-bar-2-0-e-coat",
        "category": "barbell"
    },
    "bella zinc": {
        "type": "single",
        "product_name": "The Bella Bar 2.0 - Black Zinc",
        "link": "https://www.roguefitness.com/rogue-bella-bar-2-0-black-zinc",
        "category": "barbell"
    },
    "bella ss": {
        "type": "single",
        "product_name": "The Bella Bar 2.0 - Stainless Steel",
        "link": "https://www.roguefitness.com/the-bella-bar-2-0-stainless",
        "category": "barbell"
    },
    "bella cerakote": {
        "type": "cerakote",
        "product_name": "The Bella Bar 2.0 - Cerakote",
        "link": "https://www.roguefitness.com/the-bella-rogue-womens-bar-cerakote",
        "category": "barbell"
    },
    "barbell operator": {
        "type": "cerakote",
        "product_name": "Rogue Operator Bar 3.0",
        "link": "https://www.roguefitness.com/rogue-operator-bar-cerakote",
        "category": "barbell"
    },
    "barbell chan": {
        "type": "cerakote",
        "product_name": "Rogue Chan Bar - Cerakote",
        "link": "https://www.roguefitness.com/chan-bar-cerakote",
        "category": "barbell"
    },
    "barbell training zinc": {
        "type": "multi",
        "product_name": "Rogue 28MM Training Bar - Black Zinc",
        "link": "https://www.roguefitness.com/rogue-28mm-training-bar",
        "category": "barbell"
    },
    "barbell training cerakote": {
        "type": "cerakote",
        "product_name": "Rogue 28MM Training Bar - Cerakote",
        "link": "https://www.roguefitness.com/rogue-28mm-training-bar-cerakote",
        "category": "barbell"
    },
    "barbell b&r": {
        "type": "single",
        "product_name": "Rogue B&R Bar 2.0",
        "link": "https://www.roguefitness.com/rogue-29mm-burgener-rippetoe-bar-2-0",
        "category": "barbell"
    },
    "barbell rogue 2.0": {
        "type": "single",
        "product_name": "The Rogue Bar 2.0",
        "link": "https://www.roguefitness.com/the-rogue-bar-2-0",
        "category": "barbell"
    },
    "barbell echo 2.0": {
        "type": "single",
        "product_name": "Rogue Echo Bar 2.0",
        "link": "https://www.roguefitness.com/rogue-echo-bar",
        "category": "barbell"
    },
    "barbell freedom": {
        "type": "single",
        "product_name": "Rogue Freedom Bar - 28.5MM",
        "link": "https://www.roguefitness.com/cerakote-28-5-mm-freedom-bar",
        "category": "barbell"
    },
    "barbell iwf": {
        "type": "single",
        "product_name": "Rogue 28MM IWF Olympic Weightlifting Bar w/ Center Knurl - Bright Zinc",
        "link": "https://www.roguefitness.com/rogue-iwf-olympic-wl-bar-w-center-knurl-bright-zinc",
        "category": "barbell"
    },
    "barbell 25mm iwf zinc": {
        "type": "multi",
        "product_name": "Rogue 25MM IWF Olympic Weightlifting Bar - Bright Zinc",
        "link": "https://www.roguefitness.com/rogue-25mm-wmns-oly-bar-dome-cap",
        "category": "barbell"
    },
    "barbell 25mm iwf cerakote": {
        "type": "multi",
        "product_name": "Rogue 25MM IWF Olympic Weightlifting Bar - Cerakote",
        "link": "https://www.roguefitness.com/rogue-25mm-iwf-oly-bar-cerakote",
        "category": "barbell"
    },
    "barbell westside": {
        "type": "multi",
        "product_name": "Rogue Westside Power Bar 2.0",
        "link": "https://www.roguefitness.com/rogue-westside-power-bar-2-0",
        "category": "barbell"
    },
    "barbell toomey": {
        "type": "multi",
        "product_name": "The Bella Bar - Cerakote - Tia-Clair Toomey Edition",
        "link": "https://www.roguefitness.com/rogue-athlete-bella-bar-cerakote-toomey",
        "category": "barbell"
    },
    "barbell c-70": {
        "type": "multi",
        "product_name": "Rogue C-70 Bar",
        "link": "https://www.roguefitness.com/the-rogue-c-70-bar",
        "category": "barbell"
    },
    "barbell ssb": {
        "type": "single",
        "product_name": "SB-1 - Rogue Safety Squat Bar",
        "link": "https://www.roguefitness.com/sb-1-rogue-safety-squat-bar",
        "category": "barbell"
    },
    "barbell castro": {
        "type": "single",
        "product_name": "The Castro Bar",
        "link": "https://www.roguefitness.com/the-castro-bar",
        "category": "barbell"
    },
    "barbell squat": {
        "type": "single",
        "product_name": "Rogue 32MM Squat Bar",
        "link": "https://www.roguefitness.com/rogue-32-mm-squat-bar",
        "category": "barbell"
    },
    "bench monster 2.0": {
        "type": "monster bench",
        "product_name": "Monster Utility Bench 2.0",
        "link": "https://www.roguefitness.com/monster-utility-bench-2-0-mg-black",
        "category": "bench"
    },
    "bench flat 2.0": {
        "type": "single",
        "product_name": "Rogue Flat Utility Bench 2.0",
        "link": "https://www.roguefitness.com/rogue-flat-utility-bench",
        "category": "bench"
    },
    "bench adj 2.0": {
        "type": "multi",
        "product_name": "Rogue Adjustable Bench 2.0",
        "link": "https://www.roguefitness.com/rogue-adjustable-bench-2-0",
        "category": "bench"
    },
    "bench ab2": {
        "type": "multi",
        "product_name": "AB-2 Adjustable Bench",
        "link": "https://www.roguefitness.com/ab-2-adjustable-bench",
        "category": "bench"
    },
    "bench ab3": {
        "type": "multi",
        "product_name": "Rogue AB-3 Adjustable Bench",
        "link": "https://www.roguefitness.com/rogue-ab-3-adjustable-bench",
        "category": "bench"
    },
    "bench thompson": {
        "type": "single",
        "product_name": "Thompson Fat Pad\u2122",
        "link": "https://www.roguefitness.com/thompson-fatpad",
        "category": "bench"
    },
    "bench fatpad": {
        "type": "single",
        "product_name": "Rogue Competition Fat Pad",
        "link": "https://www.roguefitness.com/rogue-competition-fat-pad",
        "category": "bench"
    },
    "bench foldup": {
        "type": "single",
        "product_name": "Rogue Fold Up Utility Bench",
        "link": "https://www.roguefitness.com/rogue-fold-up-utility-bench",
        "category": "bench"
    },
    "bench westside 2.0": {
        "type": "multi",
        "product_name": "Rogue Westside Bench 2.0",
        "link": "https://www.roguefitness.com/rogue-westside-bench-2-0",
        "category": "bench"
    },
    "bench monster westside": {
        "type": "multi",
        "product_name": "Rogue Monster Westside Bench",
        "link": "https://www.roguefitness.com/rogue-monster-westside-bench",
        "category": "bench"
    },
    "bone 29": {
        "type": "bone",
        "product_name": "Boneyard 29mm Bars",
        "link": "https://www.roguefitness.com/rogue-29mm-boneyard-bars",
        "category": "boneyard"
    },
    "bone 28": {
        "type": "bone",
        "product_name": "Boneyard 28mm Bars",
        "link": "https://www.roguefitness.com/rogue-28mm-boneyard-bars",
        "category": "boneyard"
    },
    "bone 28.5": {
        "type": "bone",
        "product_name": "Boneyard 28.5mm Bars",
        "link": "https://www.roguefitness.com/rogue-28-5-mm-boneyard-bars",
        "category": "boneyard"
    },
    "bone dead": {
        "type": "bone",
        "product_name": "Boneyard Deadlift Bars",
        "link": "https://www.roguefitness.com/rogue-boneyard-ohio-deadlift-bar",
        "category": "boneyard"
    },
    "bone curl": {
        "type": "bone",
        "product_name": "Boneyard Curl Bars",
        "link": "https://www.roguefitness.com/rogue-boneyard-curl-bar",
        "category": "boneyard"
    },
    "bone rackable curl": {
        "type": "bone",
        "product_name": "Boneyard Rackable Curl Bars",
        "link": "https://www.roguefitness.com/boneyard-rogue-rackable-curl-bar",
        "category": "boneyard"
    },
    "bone 25": {
        "type": "bone",
        "product_name": "Rogue 25MM Boneyard Bars",
        "link": "https://www.roguefitness.com/rogue-25mm-boneyard-bars",
        "category": "boneyard"
    },
    "grab bag barbell": {
        "type": "grab bag",
        "product_name": "Used Barbells",
        "link": "https://www.roguefitness.com/miscellaneous-barbells-used",
        "category": "boneyard"
    },
    "bone oso pro": {
        "type": "bone",
        "product_name": "Boneyard OSO Pro Collars",
        "link": "https://www.roguefitness.com/boneyard-oso-pro-collars-closeout",
        "category": "boneyard"
    },
    "bike echo": {
        "type": "multi",
        "product_name": "Rogue Echo Bike",
        "link": "https://www.roguefitness.com/rogue-echo-bike",
        "category": "cardio"
    },
    "rower pm5": {
        "type": "single",
        "product_name": "Black Concept 2 Model D Rower - PM5",
        "link": "https://www.roguefitness.com/black-concept-2-model-d-rower-pm5",
        "category": "cardio"
    },
    "assault airbike": {
        "type": "multi",
        "product_name": "Assault AirBike",
        "link": "https://www.roguefitness.com/assault-airbike-and-accessories",
        "category": "cardio"
    },
    "bikeerg": {
        "type": "single",
        "product_name": "Concept 2 BikeErg",
        "link": "https://www.roguefitness.com/concept2-bike-erg",
        "category": "cardio"
    },
    "skierg": {
        "type": "multi",
        "product_name": "Concept 2 SkiErg",
        "link": "https://www.roguefitness.com/concept-2-skierg-2",
        "category": "cardio"
    },
    "db 15": {
        "type": "db15",
        "product_name": "Rogue DB-15 Loadable Dumbbell",
        "link": "https://www.roguefitness.com/rogue-loadable-dumbbells",
        "category": "cond"
    },
    "db 10": {
        "type": "multi",
        "product_name": "Rogue DB-10 Loadable Dumbbell",
        "link": "https://www.roguefitness.com/rogue-loadable-dumbbells",
        "category": "cond"
    },
    "kettlebells": {
        "type": "multi",
        "product_name": "Rogue Kettlebells",
        "link": "https://www.roguefitness.com/rogue-kettlebells",
        "category": "cond"
    },
    "kettlebells comp": {
        "type": "multi",
        "product_name": "Rogue Competition Kettlebells",
        "link": "https://www.roguefitness.com/rogue-competition-kettlebells",
        "category": "cond"
    },
    "kettlebells ecoat": {
        "type": "multi",
        "product_name": "Rogue Kettlebell - E Coat",
        "link": "https://www.roguefitness.com/rogue-kettlebell-e-coat",
        "category": "cond"
    },
    "dumbbells": {
        "type": "multi",
        "product_name": "Rogue Dumbbells",
        "link": "https://www.roguefitness.com/rogue-dumbbells",
        "category": "cond"
    },
    "dumbbell sets": {
        "type": "multi",
        "product_name": "Rogue Dumbbell Sets",
        "link": "https://www.roguefitness.com/rogue-rubber-hex-dumbbell-sets",
        "category": "cond"
    },
    "medicine balls": {
        "type": "multi",
        "product_name": "Rogue Medicine Balls",
        "link": "https://www.roguefitness.com/rogue-medicine-balls",
        "category": "cond"
    },
    "fatbells": {
        "type": "multi",
        "product_name": "Rogue Thompson Fatbells",
        "link": "https://www.roguefitness.com/rogue-thompson-fatbells",
        "category": "cond"
    },
    "dumbbell bumpers": {
        "type": "multi",
        "product_name": "Rogue Dumbbell Bumpers",
        "link": "https://www.roguefitness.com/rogue-dumbbell-bumpers",
        "category": "cond"
    },
    "dumbbells urethane": {
        "type": "multi",
        "product_name": "Rogue Urethane Dumbbells",
        "link": "https://www.roguefitness.com/rogue-urethane-dumbbells-new",
        "category": "cond"
    },
    "infinity spotter": {
        "type": "multi",
        "product_name": "Rogue Infinity Safety Spotter Arms",
        "link": "https://www.roguefitness.com/set-of-safety-spotter-arms",
        "category": "inf"
    },
    "infinity straps": {
        "type": "multi",
        "product_name": "Infinity Strap Safety System 2.0",
        "link": "https://www.roguefitness.com/infinity-strap-safety-system-2-0",
        "category": "inf"
    },
    "infinity j-cups": {
        "type": "single",
        "product_name": "Rogue Infinity J-Cup Set",
        "link": "https://www.roguefitness.com/extra-infinity-j-cup-set",
        "category": "inf"
    },
    "infinity matador": {
        "type": "single",
        "product_name": "Rogue Infinity Matador",
        "link": "https://www.roguefitness.com/rogue-infinity-matador",
        "category": "inf"
    },
    "ironmaster adj 75": {
        "type": "ironmaster",
        "product_name": "Quick-Lock Adjustable Dumbbell System 75 lb Set",
        "link": "https://www.ironmaster.com/products/quick-lock-adjustable-dumbbells-75/",
        "category": "ironmaster"
    },
    "ironmaster adj 45": {
        "type": "ironmaster",
        "product_name": "Quick-Lock Adjustable Dumbbell System 45 lb Set",
        "link": "https://www.ironmaster.com/products/quick-lock-dumbbell-system-45-lb-set/",
        "category": "ironmaster"
    },
    "ironmaster addon 120": {
        "type": "ironmaster",
        "product_name": "Quick-Lock Dumbbell \u2013 120 lb Add on Kit ",
        "link": "https://www.ironmaster.com/products/add-on-kit-to-120-lbs-quick-lock/",
        "category": "ironmaster"
    },
    "m lat pulldown stand alone": {
        "type": "single",
        "product_name": "Monster Lat Pulldown/Low Row (Stand Alone)",
        "link": "https://www.roguefitness.com/lat-pulldown-low-row-stand-alone",
        "category": "m",
    },
    "m lat pulldown rack mounted": {
        "type": "single",
        "product_name": "Monster Lat Pulldown/Low Row (Rack Mounted)",
        "link": "https://www.roguefitness.com/lat-pulldown-low-row-rackmounted",
        "category": "m",
    },
    "m spotter": {
        "type": "single",
        "product_name": "Monster Safety Spotter Arms 2.0",
        "link": "https://www.roguefitness.com/monster-safety-spotter-arms-2-0",
        "category": "m"
    },
    "m top beam": {
        "type": "custom2",
        "product_name": "Monster 43 Top Beam",
        "link": "https://www.roguefitness.com/monster-43-top-beam",
        "category": "m"
    },
    "m slinger": {
        "type": "custom2",
        "product_name": "Rogue Monster Slinger",
        "link": "https://www.roguefitness.com/rogue-monster-slinger",
        "category": "m"
    },
    "m attach post": {
        "type": "single",
        "product_name": "Rogue Monster Attachment Post",
        "link": "https://www.roguefitness.com/rogue-monster-attachment-post",
        "category": "m"
    },
    "m landmine": {
        "type": "single",
        "product_name": "Rogue Monster Landmine 2.0",
        "link": "https://www.roguefitness.com/rogue-monster-landmine-2-0",
        "category": "m"
    },
    "m monolift": {
        "type": "single",
        "product_name": "Rogue Adjustable Monolift - Monster",
        "link": "https://www.roguefitness.com/rogue-adjustable-monolift-monster",
        "category": "m"
    },
    "m mini feet": {
        "type": "single",
        "product_name": "Rogue Monster Mini Feet",
        "link": "https://www.roguefitness.com/rogue-monster-mini-feet",
        "category": "m"
    },
    "m plate storage long": {
        "type": "single",
        "product_name": "SP33100 Plate Storage Pair - Long for 3x3 Monster",
        "link": "https://www.roguefitness.com/sp33100-plate-storage-long-for-3x3-monster",
        "category": "m"
    },
    "m single post shelf": {
        "type": "multi",
        "product_name": "Monster Single Post Storage Shelf",
        "link": "https://www.roguefitness.com/monster-single-post-storage-shelf",
        "category": "m"
    },
    "m storage pin": {
        "type": "custom2",
        "product_name": "Rogue Monster Plate Storage Pin",
        "link": "https://www.roguefitness.com/rogue-monster-keyhole-keyless-plate-storage-pin",
        "category": "m"
    },
    "m j-cup pairs": {
        "type": "custom2",
        "product_name": "Monster J-Cup Pairs",
        "link": "https://www.roguefitness.com/monster-j-cup-pairs",
        "category": "m"
    },
    "m matador": {
        "type": "multi",
        "product_name": "Rogue Monster Matador",
        "link": "https://www.roguefitness.com/rogue-monster-matador",
        "category": "m"
    },
    "ah-1 articulating": {
        "type": "single",
        "product_name": "H-1 Articulating Handle Kit",
        "link": "https://www.roguefitness.com/monster-ah-1-articulating-handle-kit",
        "category": "m"
    },
    "m rhino belt squat": {
        "type": "single",
        "product_name": "Rogue Monster Rhino Belt Squat - Stand Alone",
        "link": "https://www.roguefitness.com/monster-rhino-belt-squat-stand-alone-mg-black",
        "category": "m"
    },
    "m grip triangle": {
        "type": "multi",
        "product_name": "Rogue Monster Grip Triangle",
        "link": "https://www.roguefitness.com/rogue-monster-grip-triangle",
        "category": "m"
    },
    "xm-43m crossmember": {
        "type": "single",
        "product_name": "XM-43M Monster Multi Grip Crossmember",
        "link": "https://www.roguefitness.com/xm-43m-monster-multi-grip-crossmember",
        "category": "m"
    },
    "m shackle": {
        "type": "single",
        "product_name": "Rogue Monster Shackle",
        "link": "https://www.roguefitness.com/rogue-monster-shackle",
        "category": "m"
    },
    "m utility seat": {
        "type": "single",
        "product_name": "Rogue Monster Utility Seat",
        "link": "https://www.roguefitness.com/rogue-monster-utility-seat",
        "category": "m"
    },
    "m socket": {
        "type": "custom2",
        "product_name": "Rogue Monster Socket Pull-up Bar",
        "link": "https://www.roguefitness.com/rogue-monster-socket-pull-up-bar",
        "category": "m"
    },
    "m socket curl": {
        "type": "custom2",
        "product_name": "Rogue Monster Socket Pull-up Curl Bar",
        "link": "https://www.roguefitness.com/monster-socket-pull-up-bar-curl-bar",
        "category": "m"
    },
    "m band pegs": {
        "type": "multi",
        "product_name": "Monster Band Peg 2.0 - 4 Pack",
        "link": "https://www.roguefitness.com/monster-band-pegs-2-0-4-pack",
        "category": "m"
    },
    "m knurled knob": {
        "type": "custom2",
        "product_name": "Monster Knurled Knob",
        "link": "https://www.roguefitness.com/monster-knurled-knob",
        "category": "m"
    },
    "ml spotter": {
        "type": "single",
        "product_name": "SAML-24 Monster Lite Safety Spotter Arms (Pair)",
        "link": "https://www.roguefitness.com/saml-24-monster-lite-spotter-arms-pair",
        "category": "ml"
    },
    "ml straps": {
        "type": "multi",
        "product_name": "Monster Lite Strap Safety System 2.0",
        "link": "https://www.roguefitness.com/monster-lite-strap-safety-system-2-0",
        "category": "ml"
    },
    "ml j-cups": {
        "type": "single",
        "product_name": "Monster Lite J-Cups",
        "link": "https://www.roguefitness.com/j-3358-monster-lite-j-cups",
        "category": "ml"
    },
    "ml sandwich j-cups": {
        "type": "single",
        "product_name": "Monster Lite Sandwich J-Cup Pair",
        "link": "https://www.roguefitness.com/monster-lite-sandwich-j-cup-pair",
        "category": "ml"
    },
    "ml slinger": {
        "type": "custom2",
        "product_name": "Rogue Monster Lite Slinger",
        "link": "https://www.roguefitness.com/rogue-monster-lite-slinger",
        "category": "ml"
    },
    "landmine": {
        "type": "multi",
        "product_name": "Rogue Landmines",
        "link": "https://www.roguefitness.com/landmines",
        "category": "ml"
    },
    "ml monolift": {
        "type": "multi",
        "product_name": "Rogue Adjustable Monolift - Monster Lite",
        "link": "https://www.roguefitness.com/rogue-adjustable-monolift-monster-lite",
        "category": "ml"
    },
    "ml matador": {
        "type": "single",
        "product_name": "Rogue Monster Lite Matador",
        "link": "https://www.roguefitness.com/rogue-monster-lite-matador",
        "category": "ml"
    },
    "ml plate storage long": {
        "type": "single",
        "product_name": "SP3358 Plate Storage Pair - Long for Monster Lite",
        "link": "https://www.roguefitness.com/sp3358-plate-storage-long-for-monster-lite",
        "category": "ml"
    },
    "ml pin pipe": {
        "type": "multi",
        "product_name": "Infinity/ML Pin and Pipe Safeties",
        "link": "https://www.roguefitness.com/infinity-ml-pin-pipe-safeties",
        "category": "ml"
    },
    "ml band pegs": {
        "type": "single",
        "product_name": "Rogue Monster Lite/Infinity Band Pegs - 4 Pack",
        "link": "https://www.roguefitness.com/extra-set-of-band-pegs",
        "category": "ml"
    },
    "ml adj pullup": {
        "type": "single",
        "product_name": "Rogue Monster Lite Adjustable Pull-up Bar",
        "link": "https://www.roguefitness.com/rogue-monster-lite-adjustable-pull-up-bar",
        "category": "ml"
    },
    "ml crossmember": {
        "type": "multi",
        "product_name": "Monster Lite Crossmembers",
        "link": "https://www.roguefitness.com/monster-lite-crossmembers",
        "category": "ml"
    },
    "ml shackle": {
        "type": "single",
        "product_name": "Rogue Monster Lite Shackle",
        "link": "https://www.roguefitness.com/rogue-monster-lite-shackle",
        "category": "ml"
    },
    "ml socket": {
        "type": "custom2",
        "product_name": "Rogue Monster Lite Socket Pull-up Bar",
        "link": "https://www.roguefitness.com/rogue-monster-lite-socket-pull-up-bar",
        "category": "ml"
    },
    "ml socket curl": {
        "type": "custom2",
        "product_name": "Rogue Monster Lite Socket Pull-up Curl Bar",
        "link": "https://www.roguefitness.com/ml-socket-pull-up-bar-curl-bar",
        "category": "ml"
    },
    "ml wall mount kit": {
        "type": "single",
        "product_name": "Monster Lite Rack Wall Mount Kit",
        "link": "https://www.roguefitness.com/monster-lite-rack-wall-mount-kit",
        "category": "ml"
    },
    "yoke y1": {
        "type": "multi",
        "product_name": "Y-1 Rogue Yoke",
        "link": "https://www.roguefitness.com/rogue-yoke",
        "category": "other"
    },
    "yoke y2": {
        "type": "multi",
        "product_name": "Y-2 Rogue Yoke",
        "link": "https://www.roguefitness.com/y2-yoke",
        "category": "other"
    },
    "abram ghd": {
        "type": "single",
        "product_name": "Rogue Abram GHD 2.0",
        "link": "https://www.roguefitness.com/rogue-abram-glute-ham-developer-2-0",
        "category": "other"
    },
    "m ghd": {
        "type": "multi",
        "product_name": "Rogue Monster Swing Arm GHD",
        "link": "https://www.roguefitness.com/rogue-monster-swing-arm-ghd",
        "category": "other"
    },
    "echo ghd": {
        "type": "multi",
        "product_name": "Rogue 3x3 Echo GHD",
        "link": "https://www.roguefitness.com/rogue-echo-ghd",
        "category": "other"
    },
    "dl platform": {
        "type": "multi",
        "product_name": "Rogue Deadlift Platform",
        "link": "https://www.roguefitness.com/rogue-deadlift-platform",
        "category": "other"
    },
    "plate urethane 12-sided": {
        "type": "multi",
        "product_name": "Rogue 12-Sided Urethane Grip Plate",
        "link": "https://www.roguefitness.com/rogue-12-sided-urethane-grip-plates",
        "category": "plate",
    },
    "plate hi-temp": {
        "type": "multi",
        "product_name": "Rogue Bumper Plates by Hi-Temp",
        "link": "https://www.roguefitness.com/rogue-hi-temp-bumper-plates",
        "category": "plate"
    },
    "plate gorilla": {
        "type": "single",
        "product_name": "Rogue 65 LB Gorilla Bumpers (Pair)",
        "link": "https://www.roguefitness.com/gorilla-bumpers",
        "category": "plate"
    },
    "plate hg2": {
        "type": "multi",
        "product_name": "Rogue HG 2.0 Bumper Plates",
        "link": "https://www.roguefitness.com/rogue-hg-2-0-bumper-plates",
        "category": "plate"
    },
    "plate hg2 kg": {
        "type": "multi",
        "product_name": "Rogue HG 2.0 KG Bumper Plates",
        "link": "https://www.roguefitness.com/kg-rogue-bumpers",
        "category": "plate"
    },
    "plate comp lb": {
        "type": "multi",
        "product_name": "Rogue LB Competition Plates",
        "link": "https://www.roguefitness.com/rogue-competition-plates",
        "category": "plate"
    },
    "plate comp white lb": {
        "type": "multi",
        "product_name": "Rogue LB Training 2.0 Plates (White Print)",
        "link": "https://www.roguefitness.com/rogue-lb-training-2-0-plates-white-print",
        "category": "plate"
    },
    "plate comp kg": {
        "type": "multi",
        "product_name": "Rogue KG Competition Plates (IWF)",
        "link": "https://www.roguefitness.com/rogue-kg-competition-plates-iwf",
        "category": "plate"
    },
    "plate comp lb2": {
        "type": "multi",
        "product_name": "Rogue Color LB Training 2.0 Plates",
        "link": "https://www.roguefitness.com/rogue-color-lb-training-2-0-plates",
        "category": "plate"
    },
    "plate black lb": {
        "type": "multi",
        "product_name": "Rogue Black Training LB Plates",
        "link": "https://www.roguefitness.com/rogue-black-training-lb-color-stripe-plates",
        "category": "plate"
    },
    "plate black lb2": {
        "type": "multi",
        "product_name": "Rogue LB Training 2.0 Plates",
        "link": "https://www.roguefitness.com/rogue-lb-training-2-0-plates",
        "category": "plate"
    },
    "plate black kg": {
        "type": "multi",
        "product_name": "Rogue Black Training KG Plates",
        "link": "https://www.roguefitness.com/rogue-black-training-kg-striped-plates",
        "category": "plate"
    },
    "plate training kg": {
        "type": "multi",
        "product_name": "Rogue KG Training 2.0 Plates",
        "link": "https://www.roguefitness.com/rogue-kg-training-2-0-plates",
        "category": "plate"
    },
    "plate color training kg": {
        "type": "multi",
        "product_name": "Rogue Color KG Training 2.0 Plates (IWF)",
        "link": "https://www.roguefitness.com/rogue-color-kg-training-2-0-plates-iwf",
        "category": "plate"
    },
    "plate echo v2": {
        "type": "multi",
        "product_name": "Rogue Echo Bumper Plates V2",
        "link": "https://www.roguefitness.com/rogue-echo-bumper-plates-with-white-text",
        "category": "plate"
    },
    # "plate echo v1": {
    #     "type": "multi",
    #     "product_name": "Rogue Echo Bumper Plates V1",
    #     "link": "https://www.roguefitness.com/rogue-echo-bumper-plates-with-white-text-v1",
    #     "category": "plate"
    # },
    "plate echo color": {
        "type": "multi",
        "product_name": "Rogue Color Echo Bumper Plates",
        "link": "https://www.roguefitness.com/rogue-color-echo-bumper-plate",
        "category": "plate"
    },
    "plate machined": {
        "type": "multi",
        "product_name": "Rogue Machined Olympic Plates",
        "link": "https://www.roguefitness.com/rogue-machined-olympic-plates",
        "category": "plate"
    },
    "plate fleck": {
        "type": "multi",
        "product_name": "Rogue Fleck Plate",
        "link": "https://www.roguefitness.com/rogue-fleck-plates",
        "category": "plate"
    },
    "plate olympic": {
        "type": "multi",
        "product_name": "Rogue Olympic Plates",
        "link": "https://www.roguefitness.com/rogue-olympic-plates",
        "category": "plate"
    },
    "plate cal": {
        "type": "multi",
        "product_name": "Rogue Calibrated LB Steel Plates",
        "link": "https://www.roguefitness.com/rogue-calibrated-lb-steel-plates",
        "category": "plate"
    },
    "plate technique": {
        "type": "multi",
        "product_name": "Rogue Technique Plates",
        "link": "https://www.roguefitness.com/rogue-technique-plates",
        "category": "plate"
    },
    "plate change": {
        "type": "multi",
        "product_name": "Rogue LB Change Plates",
        "link": "https://www.roguefitness.com/rogue-lb-change-plates",
        "category": "plate"
    },
    "plate change kg": {
        "type": "multi",
        "product_name": "Rogue KG Change Plates (IWF)",
        "link": "https://www.roguefitness.com/rogue-kg-change-plates",
        "category": "plate"
    },
    "plate add on change": {
        "type": "multi",
        "product_name": "Rogue Add-On Change Plate Pair",
        "link": "https://www.roguefitness.com/rogue-add-on-change-plate-pair",
        "category": "plate"
    },
    "plate friction change": {
        "type": "multi",
        "product_name": "Rogue Friction Grip KG Change Plates (IWF)",
        "link": "https://www.roguefitness.com/rogue-friction-grip-kg-change-plates-iwf",
        "category": "plate"
    },
    "plate mil spec": {
        "type": "multi",
        "product_name": "Rogue US-MIL Spec Bumper",
        "link": "https://www.roguefitness.com/rogue-us-mil-sprc-bumper-plates",
        "category": "plate"
    },
    "plate mil spec echo": {
        "type": "multi",
        "product_name": "Rogue MIL Spec Echo Bumper",
        "link": "https://www.roguefitness.com/rogue-mil-echo-bumper-plates-black",
        "category": "plate"
    },
    "plate 6-shooter": {
        "type": "multi",
        "product_name": "Rogue 6-Shooter Olympic Grip Plates",
        "link": "https://www.roguefitness.com/rogue-6-shooter-olympic-plates",
        "category": "plate"
    },
    "plate cal kg": {
        "type": "multi",
        "product_name": "Rogue Calibrated KG Steel Plates",
        "link": "https://www.roguefitness.com/rogue-calibrated-kg-steel-plates",
        "category": "plate"
    },
    "plate urethane": {
        "type": "multi",
        "product_name": "Rogue Urethane Plates",
        "link": "https://www.roguefitness.com/rogue-urethane-plates",
        "category": "plate"
    },
    "plate wagon": {
        "type": "single",
        "product_name": "Rogue 26 ER Wagon Wheel Pair",
        "link": "https://www.roguefitness.com/rogue-26-er-wagon-wheel-pair",
        "category": "plate"
    },
    "plate 6-shooter urethane": {
        "type": "multi",
        "product_name": "Rogue 6-Shooter Urethane Olympic Grip Plates",
        "link": "https://www.roguefitness.com/rogue-6-shooter-urethane-olympic-grip-plates",
        "category": "plate"
    },
    "plate hi-temp comp": {
        "type": "multi",
        "product_name": "Rogue Hi-Temp Competition Training Plates",
        "link": "https://www.roguefitness.com/rogue-hi-temp-competition-training-plates",
        "category": "plate"
    },
    "plate fractional lb": {
        "type": "multi",
        "product_name": "Rogue LB Fractional Plates",
        "link": "https://www.roguefitness.com/rogue-lb-fractional-plates",
        "category": "plate"
    },
    "plate fractional kg": {
        "type": "multi",
        "product_name": "Rogue KG Fractional Plates",
        "link": "https://www.roguefitness.com/rogue-kg-fractional-plates",
        "category": "plate"
    },
    "plate york": {
        "type": "multi",
        "product_name": "York Legacy Iron Plates",
        "link": "https://www.roguefitness.com/york-legacy-iron-plates",
        "category": "plate"
    },
    "rack rml-390f": {
        "type": "multi",
        "product_name": "RML-390F Flat Foot Monster Lite Rack",
        "link": "https://www.roguefitness.com/rml-390f-flat-foot-monster-lite-rack",
        "category": "rack"
    },
    "rack rml-490": {
        "type": "multi",
        "product_name": "Rogue RML-490 Power Rack",
        "link": "https://www.roguefitness.com/rogue-rml-490-power-rack",
        "category": "rack"
    },
    "rack rml-490c": {
        "type": "rmlc",
        "product_name": "Rogue RML-490C Power Rack 3.0",
        "link": "https://www.roguefitness.com/rogue-rml-490-power-rack-color-3-0",
        "category": "rack"
    },
    "rack rml-690": {
        "type": "multi",
        "product_name": "Rogue RML-690 Power Rack",
        "link": "https://www.roguefitness.com/rml-690-power-rack",
        "category": "rack"
    },
    "rack r-3": {
        "type": "multi",
        "product_name": "Rogue R-3 Power Rack",
        "link": "https://www.roguefitness.com/rogue-r-3-power-rack",
        "category": "rack"
    },
    "rack rm-3 fortis": {
        "type": "multi",
        "product_name": "Rogue RM-3 Fortis Rack",
        "link": "https://www.roguefitness.com/rogue-rm-3-fortis-rack",
        "category": "rack"
    },
    "rack rm-4 fortis": {
        "type": "multi",
        "product_name": "Rogue RM-4 Fortis Rack",
        "link": "https://www.roguefitness.com/rogue-rm-4-fortis-rack",
        "category": "rack"
    },
    "combo rack": {
        "type": "single",
        "product_name": "Rogue Combo Rack",
        "link": "https://www.roguefitness.com/rogue-combo-rack",
        "category": "rack"
    },
    "rack r-3bt": {
        "type": "multi",
        "product_name": "Rogue Bolt-Together R-3",
        "link": "https://www.roguefitness.com/rogue-bolt-together-r-3",
        "category": "rack"
    },
    "rack rml-3fullw": {
        "type": "rmlc",
        "product_name": "Monster Lite RML-390FULLW Fold Back Wall Mount Power Rack",
        "link": "https://www.roguefitness.com/monster-lite-rml-390-fullw-fold-back-wall-mount-power-rack",
        "category": "rack"
    },
    "hr-2 conversion": {
        "type": "multi",
        "product_name": "HR-2 Half Rack Conversion Kit",
        "link": "https://www.roguefitness.com/infinity-hr2-half-rack-conversion-kit",
        "category": "rack"
    },
    "rack rml-390c": {
        "type": "rmlc",
        "product_name": "Rogue RML-390C Power Rack 3.0",
        "link": "https://www.roguefitness.com/rml-390c-power-rack-3-0",
        "category": "rack"
    },
    "rack rml-690c": {
        "type": "rmlc",
        "product_name": "Rogue RML-690C Power Rack 3.0",
        "link": "https://www.roguefitness.com/rml-690c-power-rack-3-0",
        "category": "rack"
    },
    "conversion s1 s2": {
        "type": "multi",
        "product_name": "S-1 to S-2 Conversion Kit",
        "link": "https://www.roguefitness.com/s-1-to-s-2-conversion-kit",
        "category": "rack"
    },
    "curl cerakote": {
        "type": "single",
        "product_name": "Rogue Curl Bar - Cerakote",
        "link": "https://www.roguefitness.com/rogue-curl-bar-cerakote",
        "category": "spec_bar"
    },
    "curl": {
        "type": "multi",
        "product_name": "Rogue Curl Bar",
        "link": "https://www.roguefitness.com/rogue-curl-bar",
        "category": "spec_bar"
    },
    "curl rackable": {
        "type": "single",
        "product_name": "Rogue Rackable Curl Bar",
        "link": "https://www.roguefitness.com/rogue-rackable-curl-bar",
        "category": "spec_bar"
    },
    "camber bar": {
        "type": "single",
        "product_name": "CB-1 Rogue Camber Bar",
        "link": "https://www.roguefitness.com/cb-1-rogue-camber-bar",
        "category": "spec_bar"
    },
    "trap tb1": {
        "type": "single",
        "product_name": "Rogue TB-1 Trap Bar 2.0",
        "link": "https://www.roguefitness.com/rogue-tb-1-trap-bar-2-0",
        "category": "spec_bar"
    },
    "trap tb2": {
        "type": "single",
        "product_name": "Rogue TB-2 Trap Bar",
        "link": "https://www.roguefitness.com/rogue-tb-2-trap-bar",
        "category": "spec_bar"
    },
    "mg-2 multi grip": {
        "type": "multi",
        "product_name": "Rogue MG-2 Multi Grip Bars",
        "link": "https://www.roguefitness.com/rogue-mg-2-multi-grip-bars",
        "category": "spec_bar"
    },
    "mg-3 multi grip": {
        "type": "multi",
        "product_name": "Rogue MG-3 Multi Grip Bar",
        "link": "https://www.roguefitness.com/rogue-mg-3-multi-grip-bar",
        "category": "spec_bar"
    },
    "squat sml-2": {
        "type": "multi",
        "product_name": "SML-2 Rogue 90\" Monster Lite Squat Stand",
        "link": "https://www.roguefitness.com/sml-2-rogue-90-monster-lite-squat-stand",
        "category": "squat_stand"
    },
    "squat sml-3": {
        "type": "multi",
        "product_name": "SML-3 Rogue 108\" Monster Lite Squat Stand",
        "link": "https://www.roguefitness.com/sml-3-rogue-108-monster-lite-squat-stand",
        "category": "squat_stand"
    },
    "squat s-1": {
        "type": "multi",
        "product_name": "Rogue S-1 Squat Stand 2.0",
        "link": "https://www.roguefitness.com/rogue-s-1-squat-stand-2-0",
        "category": "squat_stand"
    },
    "squat s-2": {
        "type": "multi",
        "product_name": "Rogue S-2 Squat Stand 2.0",
        "link": "https://www.roguefitness.com/rogue-s2-squat-stand-2-0",
        "category": "squat_stand"
    },
    "squat s-4": {
        "type": "multi",
        "product_name": "Rogue S-4 Squat Stand 2.0",
        "link": "https://www.roguefitness.com/rogue-s-4-squat-stand-2",
        "category": "squat_stand"
    },
    "squat echo": {
        "type": "multi",
        "product_name": "Rogue Echo Squat Stand 2.0",
        "link": "https://www.roguefitness.com/rogue-echo-squat-stand-2-0",
        "category": "squat_stand"
    },
    "plate tree": {
        "type": "multi",
        "product_name": "Rogue Vertical Plate Tree 2.0",
        "link": "https://www.roguefitness.com/rogue-vertical-plate-tree-2-0",
        "category": "storage"
    },
    "uk echo color": {
        "type": "multi",
        "product_name": "UK Rogue Color Echo Bumper Plates",
        "link": "https://www.rogueeurope.eu/rogue-color-echo-bumper-plate-eu",
        "category": "uk"
    },
    "uk echo": {
        "type": "multi",
        "product_name": "UK Rogue Echo Bumper Plates V2",
        "link": "https://www.rogueeurope.eu/rogue-echo-bumper-plates-with-white-text-eu",
        "category": "uk"
    },
    "uk p-4 pullup": {
        "type": "single",
        "product_name": "Rogue P-4 Pull-up System",
        "link": "https://www.rogueeurope.eu/rogue-p-4-pull-up-system",
        "category": "uk"
    },
    "uk rr plate": {
        "type": "multi",
        "product_name": "UK Rogue RR Plates",
        "link": "https://www.rogueeurope.eu/rogue-rr-bumper-plates-eu",
        "category": "uk"
    },
    "uk bella zinc": {
        "type": "single",
        "product_name": "UK The Bella Bar 2.0 - Black Zinc",
        "link": "https://www.rogueeurope.eu/rogue-bella-bar-eu",
        "category": "uk"
    },
    "uk opb ss": {
        "type": "single",
        "product_name": "UK Rogue 20KG Ohio Power Bar - Stainless Steel",
        "link": "https://www.rogueeurope.eu/rogue-20-kg-ohio-power-bar-stainless-steel-eu",
        "category": "uk"
    },
    "uk opb zinc": {
        "type": "single",
        "product_name": "UK Rogue 20KG Ohio Power Bar - Black Zinc",
        "link": "https://www.rogueeurope.eu/rogue-20-kg-ohio-power-bar-black-zinc-eu",
        "category": "uk"
    },
    "uk kettlebells": {
        "type": "multi",
        "product_name": "UK Rogue Kettlebells",
        "link": "https://www.rogueeurope.eu/rogue-kettlebells-eu",
        "category": "uk"
    },
    "uk dumbbells": {
        "type": "multi",
        "product_name": "UK Rogue KG Dumbbells",
        "link": "https://www.rogueeurope.eu/rogue-kg-dumbbells",
        "category": "uk"
    },
    "uk home timer": {
        "type": "multi",
        "product_name": "UK Rogue Home Timer",
        "link": "https://www.rogueeurope.eu/rogue-home-timer-eu",
        "category": "uk"
    },
    "uk plate tree": {
        "type": "multi",
        "product_name": "UK Rogue Vertical Plate Tree 2.0",
        "link": "https://www.rogueeurope.eu/rogue-vertical-plate-tree-2-0-eu",
        "category": "uk"
    },
    "uk bench ab2": {
        "type": "multi",
        "product_name": "UK AB-2 Adjustable Bench",
        "link": "https://www.rogueeurope.eu/ab-2-adjustable-bench-eu",
        "category": "uk"
    }
}
