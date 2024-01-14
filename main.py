import streamlit as st
import pandas as pd
import uuid
import os


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

st.title("CASINO")
dates_played = []

for row in st.session_state["rows"]:
    
    row_data = generate_row(row)
    rows_collection.append(row_data)
    #dates_played.append(str(dates))

entries = pd.DataFrame(rows_collection)
entries.dropna(inplace = True)
#st.write(pd.DataFrame(rows_collection))


menu = st.columns(2)
with menu[0]:
    st.button("Add Games/Entries", on_click=add_row)


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

Balances = {"Games": balances.keys(), "Balance ($)": balances.values()}

total_balance = sum(balances.values())
T_balance = 'Total Balance $' + str(total_balance)
if total_balance >= 0: 
    new_title = f'<p style="font-family:sans-serif; color:Green; font-size: 32px;">{T_balance}</p>'
else: 
    new_title = f'<p style="font-family:sans-serif; color:Red; font-size: 32px;">{T_balance}</p>'

st.markdown(new_title, unsafe_allow_html=True)
#st.title(new_title)
df_games = pd.DataFrame(Balances).set_index('Games').rename_axis('Games')
#df_games.drop(index = 'Games', inplace = True)
df_2 = df_games.style.applymap(lambda x: 'color: red' if int(x) < 0 else 'color: green')
#st.dataframe(df_2)

#st.write(df_2.to_html(), unsafe_allow_html= True)
############ Styles
th_props = [('font-size', '12px'), ('text-align', 'center'), ('font-weight','bold'), ('color', '#6d6d6d')]
td_props = [('font-size', '12px')]
styles = [dict(selector = 'th', props = th_props), dict(selector = 'td', props = td_props)]
###########
#df_2 = df_games.set_table_style(styles)
#df_games.rename_axis("Games")
st.table(df_2)

with menu[1]:

    if st.button("End & Submit Entries"):

        final_table.to_csv("Casino.csv")


#df_balance = pd.DataFrame(rows_collection)


    # if os.path.isfile("Casino.csv"): 
    #     casino_df = pd.read_csv('Casino.csv')
    #     try: 
    #         casino_df.drop('Unnamed: 0', axis = 1, inplace = True)
    #     except: 
    #         pass

    #     df_balance = pd.concat([df_balance, casino_df], ignore_index=True)
    # else: 
    #     pass 
# df_balance.to_csv("Casino.csv", index = False)

#st.write(data)
#st.write(casino_df)

#if len(rows_collection) > 0:
    #st.subheader("Collected Data")
    #display = st.columns(3)
    #data = pd.DataFrame(rows_collection)
    #data.to_csv("Casino.csv", mode='a', index= False, header = False)
    #st.write(data)
    #data.rename(columns={"name": "Item Name", "Buyin": "Buyin", "Cashout": "Cashout"}, inplace=True)
    #display[0].dataframe(data=data, use_container_width=True)
    #display[1].bar_chart(data=data, x="Item Name", y="Quantity")



