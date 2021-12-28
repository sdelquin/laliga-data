from laliga.competition import Competition

comp = Competition()
comp.get_competition_data(2)
comp.to_csv()
