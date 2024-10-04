import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def update_paid_days(signup_month_start, channel, signup_value):
    increments_start = 1

    # I'd consider a groupby apply here (I can see the need to iterate progressively through increments
    #   , but could be more efficient to groupby apply on channels)
    while signup_month_start <= pd.to_datetime('2024-08-01'):
        channel_month_ind = (signup_value.channels == channel) & (signup_value.signup_month == signup_month_start)
        # Take the first unpopulated increment, this MIGHT run into issues for thin channels where we project 0 paid days, but probably fine
        increments_start = signup_value.loc[
            channel_month_ind & (signup_value.paid_days == 0), 
            'increments_from_signup'].min()

        while increments_start <= 18:
            ## For projection periods <= 18, update projected_paid_days (t) with projected_paid_days (t-1) * ds_curve (t)
            # Young man this line is far too long! Break it up! Also please add more comments (I know we're working fast, but it'll save you time later)

            # Simpler to get the filtered ind first, then get locs
            
            prev_paid_days = signup_value.loc[
                channel_month_ind & (signup_value.increments_from_signup == increments_start-1),
                'projected_paid_days'].values[0]
            ds_curve = signup_value.loc[
                channel_month_ind & (signup_value.increments_from_signup == increments_start), 
                'ds_curve'].values[0]
            signup_value.loc[
                channel_month_ind & (signup_value.increments_from_signup == increments_start)
                , 'projected_paid_days'] = prev_paid_days*ds_curve

            increments_start += 1
        
        signup_month_start = signup_month_start + pd.DateOffset(months=1)

# Won't go through this, need to explain how this is differnt from the above? Consider just very quick docstrings
def update_paid_days_historical(signup_month_start, channel, signup_value):
    increments_start = 1

    while signup_month_start <= pd.to_datetime('2024-08-01'):
        increments_start = signup_value.loc[(signup_value.channels == channel) & (signup_value.signup_month == signup_month_start) & (signup_value.projected_paid_days == 0), 'increments_from_signup'].min()

        while increments_start <= 60:
            ## For projection periods >= 19, update projected_paid_days (t) with projected_paid_days (t-1) * avg_historical_curve (t)
            prev_paid_days = signup_value.loc[(signup_value.channels == channel) & (signup_value.signup_month == signup_month_start) & (signup_value.increments_from_signup == increments_start-1), 'projected_paid_days'].values[0]
            avg_curve = signup_value.loc[(signup_value.channels == channel) & (signup_value.signup_month == signup_month_start) & (signup_value.increments_from_signup == increments_start), 'avg_historical_curve'].values[0]
            signup_value.loc[(signup_value.channels == channel) & (signup_value.signup_month == signup_month_start) & (signup_value.increments_from_signup == increments_start), 'projected_paid_days'] = prev_paid_days*avg_curve

            increments_start += 1
        
        signup_month_start = signup_month_start + pd.DateOffset(months=1)


def google_plot(summary_all):
    _, axes = plt.subplots(4, 1, figsize = (13,15))
    plt.subplots_adjust(hspace=0.5)

    # The below is far more elegant, don't repeat yourself!! Copilot very nifty for these updates :)
    for ax, channel in zip(axes.flatten(), ['Google_Desktop', 'Google_Mobile', 'Google_Desktop_Brand', 'Google_Mobile_Brand']):
        for metric, color, name in zip(['12_mo_pcp_per_signup', '60_mo_pcp_per_signup', 'realized_pcp_per_signup', 'cps'], ['lightgreen', 'green', 'blue', 'red'], ['12-month PCP', '60-month PCP', 'Actual PCP', 'CPS']):
            ax.plot('signup_month', metric, '--' if metric != 'cps' else '-', label = name, marker = '.', color=color, data = summary_all.loc[summary_all.channels==channel])
        ax1 = ax.twinx()
        ax1.bar(data = summary_all.loc[summary_all.channels==channel], 
                    x='signup_month', height='signups', label = 'Signups', width=20, color='blue', alpha=0.2)
        ax.set_title(channel, fontweight='bold')
        ax.set_ylabel('$/Signup')
        ax1.set_ylabel('Signups')
        ## Combine legends between the two axes into a single legend
        h1, l1 = ax.get_legend_handles_labels()
        h2, l2 = ax1.get_legend_handles_labels()
        ax.legend(h1 + h2, l1 + l2, bbox_to_anchor=(1.1, 1), loc='upper left', borderaxespad=0.)


    plt.show()