from laliga.competition import Competition

comp = Competition()
comp.get_competition_data()
comp.to_dataframe()
comp.to_csv()
