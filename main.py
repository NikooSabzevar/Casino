import streamlit as st
import pandas as pd
import uuid
import os
import time
import keyboard
import sys
import psutil


if "rows" not in st.session_state:
    st.session_state["rows"] = []

rows_collection = []

def add_row():
    element_id = uuid.uuid4()
    st.session_state["rows"].append(str(element_id))


def remove_row(row_id):
    st.session_state["rows"].remove(str(row_id))


def generate_row(row_id):
    row_container = st.empty()
    row_columns = row_container.columns((5, 4, 3, 2, 1))
    row_name = row_columns[1].selectbox("game", ["Poker", "Crabs", "Blackjack", "Roulette", "Slots"], index=None, placeholder="games...", key=f"txt_{row_id}")
    
    dates = row_columns[0].date_input('dates played', value=None, key=f"nbr_{row_id}_0")
    row_qty1 = row_columns[2].number_input("$ buyin", step=1, key=f"nbr_{row_id}_1")
    row_qty2 = row_columns[3].number_input("$ cashout", step=1, key=f"nbr_{row_id}_2")

    row_columns[4].button("🗑️", key=f"del_{row_id}", on_click=remove_row, args=[row_id])
    return {"dates": dates, "game": row_name, "buyin": row_qty1, 'cashout': row_qty2}

st.title("CASINO TRACKER")

for row in st.session_state["rows"]:
    
    row_data = generate_row(row)
    rows_collection.append(row_data)

entries = pd.DataFrame(rows_collection)
entries.dropna(inplace = True)


if os.path.isfile("Casino.csv"): 
    casino_df = pd.read_csv('Casino.csv')
    try: 
        casino_df.drop('Unnamed: 0', axis = 1, inplace = True)
    except: 
        pass
else: 
    casino_df = pd.DataFrame()

final_table = pd.concat([entries, casino_df], ignore_index= True)

#st.write(final_table)

balances = {'Poker': 0, "Crabs": 0, "Blackjack": 0, "Roulette": 0, "Slots": 0}

try:
    balances['Poker'] = final_table[final_table['game'] == "Poker"]['cashout'].sum() - final_table[final_table['game'] == "Poker"]['buyin'].sum()
    balances['Crabs'] = final_table[final_table['game'] == "Crabs"]['cashout'].sum() - final_table[final_table['game'] == "Crabs"]['buyin'].sum()
    balances['Blackjack'] = final_table[final_table['game'] == "Blackjack"]['cashout'].sum() - final_table[final_table['game'] == "Blackjack"]['buyin'].sum()
    balances['Roulette'] = final_table[final_table['game'] == "Roulette"]['cashout'].sum() - final_table[final_table['game'] == "Roulette"]['buyin'].sum()
    balances['Slots'] = final_table[final_table['game'] == "Slots"]['cashout'].sum() - final_table[final_table['game'] == "Slots"]['buyin'].sum()

except: 
    pass

Balances = pd.DataFrame.from_dict({"Games": balances.keys(), "Balance ($)": balances.values()})
final_table['balance'] = final_table['cashout'] - final_table['buyin']


menu = st.columns(2)
with menu[0]:
    st.button("Add Games/Entries", on_click=add_row)
    #Balances.to_csv('temp.csv')
    #final_table.to_csv("Casino.csv")



#@st.cache
total_balance = final_table['balance'].sum()
T_balance = 'Total Balance $' + str(total_balance)
if total_balance > 0: 
    new_title = f'<p style="font-family:sans-serif; color:Green; font-size: 32px;">{T_balance}</p>'
elif total_balance < 0: 
    new_title = f'<p style="font-family:sans-serif; color:Red; font-size: 32px;">{T_balance}</p>'
else:
    new_title = f'<p style="font-family:sans-serif; color:Black; font-size: 32px;">{T_balance}</p>'

st.markdown(new_title, unsafe_allow_html=True)
#st.title(new_title)
df_games = pd.DataFrame(Balances).set_index('Games').rename_axis('Games')
df_games['Balance ($)'].apply(lambda x: round(x, 2))


#df_games.drop(index = 'Games', inplace = True)
def color_condition(x): 
    if x < 0:
        return 'color : red'
    elif x > 0: 
        return 'color : green'
    else: 
        return 'color: black' 
    
df_2 = df_games.style.applymap(color_condition).format({"Balance ($)": "{:.1f}".format})
st.table(df_2)

###### Download as local #######
from datetime import date 

#temp_local = pd.read_csv('Casino.csv')

final_table['dates'] = pd.to_datetime(final_table['dates'])
final_table.sort_values(["dates"],  axis=0, ascending=[False], ignore_index=True, inplace=True)
try: 
    final_table.drop(['level_0', 'index'], axis = 1, inplace = True)
except: 
    pass 

#final_table.reset_index(drop = True) 
csv = final_table.to_csv()
st.download_button(label = "Download the master sheet", data = csv, file_name = str(date.today())+'.csv')


exit_app = st.sidebar.button("Submit & Close")
if exit_app:
    final_table.to_csv("Casino.csv") 
    # Give a bit of delay for user experience
    time.sleep(2)
    # Close streamlit browser tab
    keyboard.press_and_release('ctrl+w')
    # Terminate streamlit python process
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()