from features.is_today import IsToday
from features.prev7days_sales import Prev7Days
from features.sales_a_year_ago import SalesAYearAgo
from features.sales_weeks_ago import SalesWeeksAgo
from features.sma import SMA
from features.today_sales import TodaySales
from features.today_to_org_sales_corr import TodayToOrgSalesCorr

# test data location
TEST_DATA_FILE_PATH = "./TestData.csv"

SIMPLE_FEATURES = [TodaySales('today_sales'),
                   Prev7Days('prev_7_days'),
                   SalesAYearAgo('sales_a_year_ago'),
                   IsToday('is_today')]
SALES_WEEKS_AGO_FEATURES = [SalesWeeksAgo(f"sales_{x}_weeks_ago", x) for x in range(1, 13)]
SMA_DAYS_AGO_FEATURES = [SMA(f"sales_sma_{x}_days_ago", x) for x in [7, 14, 21, 28, 365]]

# list all the active features that are calculated for a location
FRAME_FEATURES = SIMPLE_FEATURES + SALES_WEEKS_AGO_FEATURES + SMA_DAYS_AGO_FEATURES

# list all the active features that are calculated for the whole organization
ORG_FEATURES = [TodayToOrgSalesCorr('today_to_org_sales_corr')]
