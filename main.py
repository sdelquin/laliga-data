from laliga.competition import Competition

comp = Competition()
comp.get_competition_data(20)
comp.to_dataframe()
comp.to_csv()
