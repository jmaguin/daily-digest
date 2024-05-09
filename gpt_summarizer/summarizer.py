import os
from dotenv import load_dotenv
from openai import OpenAI


class gpt_summarizer:
  def __init__(self):
    load_dotenv()
    self.client = OpenAI()

    self.model="gpt-3.5-turbo"
    self.sys_msg = []
    self.data_msg = []
    sys_msg=[
      "Summarize the following news articles using the following rules:",
      "1. Use all the articles listed in the summary",
      "2. Represent all perspectives in the articles fairly",
      "4. Assume all information in the articles is accurate",
      "5. keep the response within 300 words or less",
      #"6. add citations for each article used using [1], [2], [3]"
    ]
    for msg in sys_msg:
      #print(msg)
      self.sys_msg.append({"role": "system", "content": msg})


  def import_test(self):
    self.data_msg = [
      {
        "role":"user",
        "content": """
ALBANY, N.Y. (AP) — New York Gov. Kathy Hochul said Tuesday that she wants to spend $2.4 billion to help deal with the massive influx of migrants who have overwhelmed New York City’s homeless shelters — addressing a damaging political issue for Democrats in her proposed state budget.
The migrant spending plan came as part of a $233 billion budget proposal from the governor’s office that will kick off months of negotiations with legislative leaders.
How the governor planned to deal with migrants, some 70,000 of whom are in the care of New York City, had been a looming question ahead of the legislative session. She did not tackle the issue in her State of the State address last week and the word “migrant” wasn’t mentioned in her detailed 181-page policy plan book.
On Tuesday, she unveiled a plan to provide shelter services, legal assistance and more for asylum-seekers, and reiterated calls for the federal government to provide more assistance to the state.
WATCH: Rep. Cuellar on border dispute between Texas, federal officials after migrant deaths
“We’re doing this not just because it’s the right thing to do for the migrants and for the city of New York,” Hochul said at the state Capitol. “We also know that companies won’t do business in New York if there are thousands of people sleeping on the streets, or the quality of life is dramatically impacted because the city is forced to cut essential services.”
The issue has the potential to damage Democratic congressional candidates in New York this fall, with key suburban races in the state expected to heavily count toward which party controls the U.S. House. Republicans have been lobbing steady criticism at President Joe Biden and fellow Democrats over federal immigration policy, with the subject already touching races in New York.
“We have a Democratic administration in Washington that hasn’t addressed the border crisis, has not secured the border,” Assembly Republican Minority Leader Will Barclay told reporters. “I’m not thrilled to have to spend any money on the migrant crisis.”
Hochul’s plan would earmark $2.4 billion for short-term shelter services, health care and pay for larger-scale emergency housing centers that have been set up to deal with the influx of asylum seekers. It would also be used to pay for legal assistance to help migrants through the asylum and work-permitting process.
The governor told reporters she will head to Washington this week to meet with the Biden administration to discuss the migrant influx — one of many such visits she has had over the last several months.
“Until we see a change in federal policy that slows the flow of new arrivals, we’re going to be swimming against the tide,” Hochul said.
The proposed budget also provided Hochul a chance to elaborate on several policy proposals she announced last week.
She asked for $35.3 billion in education funding, in part to expand universal prekindergarten programs in school districts across the state, and said she wants $40 million for a plan to crack down on retail theft. Separately, she said spending on Medicaid would reach $35.5 billion, which would mark an increase from last year driven by greater enrollment.
The deadline for adopting a state budget is April 1.
"""
      },
      {
        "role":"user",  
        "content": """
RAFAH, Gaza Strip (AP) — Palestinian militants battled Israeli forces in devastated northern Gaza and launched a barrage of rockets from farther south on Tuesday in a show of force more than 100 days into Israel’s massive air and ground campaign against the tiny coastal enclave.
The fighting in the north, which was the first target of Israel’s offensive and where entire neighborhoods have been pulverized, showed how far Israel remains from achieving its goals of dismantling Hamas and returning scores of hostages captured in the Oct. 7 attack that sparked the war.
In other developments, France and Qatar, the Persian Gulf nation that helped mediate a previous cease-fire, said late Tuesday that they had brokered a deal between Israel and Hamas to deliver medicine to Israeli hostages in Gaza, as well as additional aid to Palestinians in the besieged territory.
WATCH: Senate debates resolution for human rights report on U.S. aid to Israel for Gaza war
France said it had been working since October on the deal, which will provide three months’ worth of medication for 45 hostages with chronic illnesses, as well as other medicines and vitamins. The medicines are expected to enter Gaza from Egypt on Wednesday.
It was the first known agreement between the warring sides since a weeklong truce in November.
Meanwhile, Gaza’s humanitarian crisis is worsening, with 85 percent of the territory’s 2.3 million Palestinians having fled their homes and U.N. agencies warning of mass starvation and disease. The conflict threatens to widen after the U.S. and Israel traded strikes with Iranian-backed groups across the region.
Israel has vowed to crush Hamas’ military and governing capabilities to ensure that the Oct. 7 attack is never repeated. Militants stormed into Israel from Gaza that day, killing some 1,200 people, mostly civilians, and capturing around 250 people. With strong diplomatic and military support from the United States, Israel has resisted international calls for a cease-fire.
Nearly half of the hostages were released during the truce, but more than 100 remain in captivity. Hamas has said it will not release any others until Israel ends the war.
A person stands in front of a fishing boat at the beach, amid the ongoing conflict between Israel and Palestinian Islamist group Hamas, in Rafah, in the southern Gaza Strip, January 16, 2024. Photo by Mohammed Salem/REUTERS
Strikes and counterstrikes across the region
The longer the war goes on, the more it threatens to ignite other fronts across the region.
Iran fired missiles late Monday at what it said were Israeli “spy headquarters” in an upscale neighborhood near the sprawling U.S. Consulate in Irbil, the seat of Iraq’s northern semi-autonomous Kurdish region. Iraq and the U.S. condemned the strikes, which killed several civilians, and Baghdad recalled its ambassador to Iran in protest.
Iranian-backed groups in Iraq and Syria have carried out dozens of attacks on bases housing U.S. forces, and a U.S. airstrike in Baghdad killed an Iranian-backed militia leader earlier this month.
Elsewhere, Iranian-backed Houthi rebels in Yemen have resumed their attacks on container ships in the Red Sea following a wave of U.S.-led strikes last week. The U.S. military carried out another strike Tuesday. Separately, it said two Navy SEALS are missing after a raid last week on a ship carrying Iranian-made missile parts and weapons bound for Yemen.
Israel and Lebanon’s Hezbollah militant group have exchanged fire along the border nearly every day since the war in Gaza began. The strikes and counterstrikes have grown more severe since an Israeli strike killed Hamas’ deputy political leader in Beirut this month, raising fears of a repeat of the 2006 war.
Militants keep fighting in Gaza’s hard-hit north
In Gaza, the Israeli military said its forces located some 100 rocket installations and 60 ready-to-use rockets in the area of Beit Lahiya, a town on the territory’s northern edge. Israeli forces killed dozens of militants during the operation, the military said, without providing evidence.
Mahmoud Abdel-Ghani, who lives in Beit Lahiya, said Israeli airstrikes hit several buildings on the eastern side of the town.
Hundreds of thousands of people fled northern Gaza, including Gaza City, following Israeli evacuation orders in October. Israel shut off water to the north in the opening days of the war, and hardly any aid has been allowed into the area, even as tens of thousands of people have remained there.
READ MORE: Video appears to show the Israeli army shooting Palestinians without provocation, killing 1 and wounding 2 others
Residents reached by phone Tuesday described the heaviest fighting in weeks in Gaza City.
“The bombing never stopped,” said Faris Abu Abbas, who lives in the Tel al-Hawa neighborhood. “The resistance is here and didn’t leave.”
Ayoub Saad, who lives near Shifa Hospital downtown, said he heard gunfire and shelling overnight and into Tuesday and saw dead and wounded people being brought to the hospital on carts.
After weeks of heavy fighting across northern Gaza, Israeli officials said at the start of the year that they were scaling back operations there. The focus shifted to the southern city of Khan Younis and built-up refugee camps in central Gaza dating back to the 1948 war surrounding Israel’s creation.
But there too, they have encountered heavy resistance. The military said at least 25 rockets were fired into Israel on Tuesday, damaging a store in one of the strongest bombardments in more than a week. Israel’s Channel 12 television said the rockets were launched from the Bureij camp in central Gaza.
A child reacts as Palestinians charge their devices outside the Emirati hospital, amid the ongoing conflict between Israel and the Palestinian Islamist group Hamas, in Rafah in the southern Gaza Strip, January 15, 2024. Photo by Ibraheem Abu Mustafa/REUTERS
A spiraling humanitarian crisis
Gaza’s Health Ministry said Tuesday that the bodies of 158 people killed in Israeli strikes have been brought to hospitals in the past 24 hours, bringing the war’s overall death toll to 24,285. The ministry does not differentiate between civilian and combatant deaths but says around two-thirds of those killed were women and children.
Senior U.N. officials warned Monday that Gaza faces widespread famine and disease if more aid is not allowed in. While they did not directly blame Israel, they said aid delivery is hobbled by the opening of too few border crossings, a slow vetting process, and continuing fighting throughout the territory — all of which is largely under Israel’s control.
WATCH: South Africa accuses Israel of genocide against Palestinians at top international court
U.N. Secretary-General Antonio Guterres said U.N. agencies and their partners “cannot effectively deliver humanitarian aid while Gaza is under such heavy, widespread and unrelenting bombardment.” At least 152 U.N. staffers have been killed in Gaza since the start of the war.
Israeli officials say they have placed no limits on humanitarian aid and have called on the U.N. to provide more workers and trucks to accelerate delivery.
Israel completely sealed off Gaza after Hamas’ Oct. 7 attack and only relented under U.S. pressure. The U.S., as well as the U.N., have continued to push Israel to ease the flow of aid.
Israel blames the high civilian death toll on Hamas because it fights in dense residential areas. Israel says its forces have killed roughly 8,000 militants, without providing evidence, and that 190 of its own soldiers have been killed in the Gaza offensive.
Magdy reported from Cairo. Lidman reported from Tel Aviv, Israel. Associated Press writers Jon Gambrell in Jerusalem and Sylvie Corbet in Paris contributed to this report.
"""
      },
      {
        "role":"user",
        "content":"""
BRUSSELS (AP) — The European Union presidency on Tuesday warned that the foundations of democracy will be put to the test during the November U.S. election, envisaging a scenario where the longstanding trans-Atlantic alliance could unravel ever more.
Prime Minister Alexander De Croo of Belgium, whose country currently holds the rotating EU presidency, said that “if 2024 brings us ‘America first’ again, it is really more than ever ‘Europe on its own.’”
De Croo spoke in an address to the EU legislature only hours after former President Donald Trump’s landslide win in the Republican Party’s Iowa caucuses.
WATCH: Republican strategist discusses Trump’s grip on GOP after Iowa win
His words harked back to the 2017-2021 Trump administration, when U.S. relations with Europe took a nosedive because of near-incessant trans-Atlantic quarrels about trade, security and military cooperation that eroded trust and cooperation.
De Croo said the 27-nation EU should quickly learn to stand more on its own and that in case of a Trump victory in November, “we should, as Europeans, not fear this perspective. We should embrace it.”
Referring to the upcoming European Parliament elections in June, he said this was “a year where our democracies and liberties will be put to the test.”
“Not only with election for this house, but equally for the U.S. Congress and the American presidency,” De Croo added.
"""
      }
    ]

  def import_data(self, data): #input array of strings: each string is a different news article
    self.data_msg = []
    for msg in data:
      self.data_msg.append({"role": "user", "content": msg})


  def summarize(self): #send Chatgpt the system and data messages and wait for the response
    if len(self.data_msg) > 0:
      self.completion = self.client.chat.completions.create(
        model=self.model,
        messages=self.sys_msg + self.data_msg
      )
    else:
      print("ERROR")
    #return completion.choices[0].message.content

  def get_summary(self): #return the generated summary as a string
    return self.completion.choices[0].message.content
  

#TESTING
#new = gpt_summarizer()
#new.import_test()
#new.summarize()
#print(new.get_summary())