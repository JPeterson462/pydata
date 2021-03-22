import pandas as pd

# Convert reddit_web.csv to a chart of daily post volume

raw_dataset = pd.read_csv('reddit_wsb.csv')

post_dates = raw_dataset["timestamp"].tolist()
for index in range(len(post_dates)):
    post_dates[index] = post_dates[index].split(" ")[0]
post_dates = list(set(post_dates))


with open('wsb_daily_volume.csv', 'w') as f:
    f.write("date,volume\n")
    for post_date in post_dates:
        posts_on_this_day = raw_dataset[raw_dataset['timestamp'].str.contains(post_date)]
        num_posts_on_this_day = posts_on_this_day.shape[0]
        f.write("'%s',%d\n" % (post_date, num_posts_on_this_day))
    f.close()
