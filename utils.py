import pandas as pd
import matplotlib.pyplot as plt

def update_paid_days(signup_month_start, channel, signup_value):
    increments_start = 1

    while signup_month_start <= pd.to_datetime('2024-08-01'):
        increments_start = signup_value.loc[(signup_value.channels == channel) & (signup_value.signup_month == signup_month_start) & (signup_value.paid_days == 0), 'increments_from_signup'].min()

        while increments_start <= 18:
            ## For projection periods <= 18, update projected_paid_days (t) with projected_paid_days (t-1) * ds_curve (t) 
            prev_paid_days = signup_value.loc[(signup_value.channels == channel) & (signup_value.signup_month == signup_month_start) & (signup_value.increments_from_signup == increments_start-1), 'projected_paid_days'].values[0]
            ds_curve = signup_value.loc[(signup_value.channels == channel) & (signup_value.signup_month == signup_month_start) & (signup_value.increments_from_signup == increments_start), 'ds_curve'].values[0]
            signup_value.loc[(signup_value.channels == channel) & (signup_value.signup_month == signup_month_start) & (signup_value.increments_from_signup == increments_start), 'projected_paid_days'] = prev_paid_days*ds_curve

            increments_start += 1
        
        signup_month_start = signup_month_start + pd.DateOffset(months=1)


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
    fig, axes = plt.subplots(4, 1, figsize = (13,15))
    plt.subplots_adjust(hspace=0.5)

    # Google Desktop
    axes[0].plot('signup_month', '12_mo_pcp_per_signup', '--', label = '12-month PCP', marker = '.', color='lightgreen', data = summary_all.loc[summary_all.channels=='Google_Desktop'])
    axes[0].plot('signup_month', '60_mo_pcp_per_signup', '--', label = '60-month PCP', marker = '.', color='green', data = summary_all.loc[summary_all.channels=='Google_Desktop'])
    axes[0].plot('signup_month', 'realized_pcp_per_signup', '-', label = 'Actual PCP', marker = '.', color='blue', data = summary_all.loc[summary_all.channels=='Google_Desktop'])
    axes[0].plot('signup_month', 'cps', '-', label = 'CPS', marker = '.', color='red', data = summary_all.loc[summary_all.channels=='Google_Desktop'])
    axes[0].set_title('Google Desktop', fontweight='bold')
    axes[0].set_ylabel('PCP')
    axes[0].legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    # Google Mobile
    axes[1].plot('signup_month', '12_mo_pcp_per_signup', '--', label = '12-month PCP', marker = '.', color='lightgreen', data = summary_all.loc[summary_all.channels=='Google_Mobile'])
    axes[1].plot('signup_month', '60_mo_pcp_per_signup', '--', label = '60-month PCP', marker = '.', color='green', data = summary_all.loc[summary_all.channels=='Google_Mobile'])
    axes[1].plot('signup_month', 'realized_pcp_per_signup', '-', label = 'Actual PCP', marker = '.', color='blue', data = summary_all.loc[summary_all.channels=='Google_Mobile'])
    axes[1].plot('signup_month', 'cps', '-', label = 'CPS', marker = '.', color='red', data = summary_all.loc[summary_all.channels=='Google_Mobile'])
    axes[1].set_title('Google Mobile', fontweight='bold')
    axes[1].set_ylabel('PCP')
    axes[1].legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    # Google Desktop Brand
    axes[2].plot('signup_month', '12_mo_pcp_per_signup', '--', label = '12-month PCP', marker = '.', color='lightgreen', data = summary_all.loc[summary_all.channels=='Google_Desktop_Brand'])
    axes[2].plot('signup_month', '60_mo_pcp_per_signup', '--', label = '60-month PCP', marker = '.', color='green', data = summary_all.loc[summary_all.channels=='Google_Desktop_Brand'])
    axes[2].plot('signup_month', 'realized_pcp_per_signup', '-', label = 'Actual PCP', marker = '.', color='blue', data = summary_all.loc[summary_all.channels=='Google_Desktop_Brand'])
    axes[2].plot('signup_month', 'cps', '-', label = 'CPS', marker = '.', color='red', data = summary_all.loc[summary_all.channels=='Google_Desktop_Brand'])
    axes[2].set_title('Google Desktop Brand', fontweight='bold')
    axes[2].set_ylabel('PCP')
    axes[2].legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)


    # Google Mobile Brand
    axes[3].plot('signup_month', '12_mo_pcp_per_signup', '--', label = '12-month PCP', marker = '.', color='lightgreen', data = summary_all.loc[summary_all.channels=='Google_Mobile_Brand'])
    axes[3].plot('signup_month', '60_mo_pcp_per_signup', '--', label = '60-month PCP', marker = '.', color='green', data = summary_all.loc[summary_all.channels=='Google_Mobile_Brand'])
    axes[3].plot('signup_month', 'realized_pcp_per_signup', '-', label = 'Actual PCP', marker = '.', color='blue', data = summary_all.loc[summary_all.channels=='Google_Mobile_Brand'])
    axes[3].plot('signup_month', 'cps', '-', label = 'CPS', marker = '.', color='red', data = summary_all.loc[summary_all.channels=='Google_Mobile_Brand'])
    axes[3].set_title('Google Mobile Brand', fontweight='bold')
    axes[3].set_ylabel('PCP')
    axes[3].legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    plt.show()