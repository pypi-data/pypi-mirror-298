# Import packages
import json
import pandas as pd
import numpy as np
import requests
import ratelimit
import datetime
import os

# Node class and respective functions
"""
Tree class
"""

class Node():
    def __init__(self, name, children=None, parent=None, attribute=None):
        self.name = name
        self.children = []
        self.parent = parent
        self.attribute = attribute

        if children is not None:
            for child in children:
                child.parent = self

        if parent is not None:
            parent.addNode(self)

    def addNode(self, obj):
        """
        Add the child "obj" to the node "self"
        """
        self.children.append(obj)
        obj.parent = self

    def getRootParent(self):
        """
        Returns the root parent node of a given node
        """
        while (self.parent != None):
            self = self.parent

        return self

    def getChildrenNames(self):
        return [child.name for child in self.children]

    def getChildrenNodes(self):
        return self.children

    def dfs(self, visited):
        """
        A depth-first search function that takes in a Node class and an empty list "visited", returning a list of all the children of that Node
        """
        visited.append(self.name)

        for child in self.children:
            child.dfs(visited)

        return visited


# API connection class

class Ticker():

    def __init__(self, ticker):
        self.ticker = ticker
        self.cik = self.CIK()
        self.data = self.SEC()
        self.SIC = self.SIC()

    def CIK(self):
        try:
            headers = {"Accept": "application/json, text/plain, */*",
                       "Accept-Language": "en-US,en;q=0.9",
                       "Origin": "https://www.nasdaq.com",
                       "Referer": "https://www.nasdaq.com",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

            source = requests.get(url="https://www.sec.gov/files/company_tickers.json", headers=headers, verify=True)
            cik = source.json()

        except:
            this_dir, this_filename = os.path.split(__file__)
            source = os.path.join(this_dir, "data", "company_tickers.json")

            with open(source) as f:
                cik = json.load(f)

        cik = pd.DataFrame(cik)
        cik = cik.transpose()

        value = str(cik.loc[cik["ticker"] == self.ticker]["cik_str"].iloc[0])

        # Making sure the CIK is of right length
        value = value.zfill(10)

        return value

    def is_date_between(self, date, q):

        start_date = q[0]
        end_date = q[1]

        date_month = date.month
        date_day = date.day

        start_month = start_date.month
        start_day = start_date.day

        end_month = end_date.month
        end_day = end_date.day

        if start_month < end_month:
            return (start_month, start_day) <= (date_month, date_day) <= (end_month, end_day)
        elif start_month > end_month:
            return (start_month, start_day) <= (date_month, date_day) or (date_month, date_day) <= (end_month, end_day)
        else:  # start_month == end_month
            if start_day <= end_day:
                return (start_month, start_day) <= (date_month, date_day) <= (end_month, end_day)
            else:  # Handle wraparound from end of year to start of year
                return (start_month, start_day) <= (date_month, date_day) or (date_month, date_day) <= (
                    end_month, end_day)

    def SIC(self):
        this_dir, this_filename = os.path.split(__file__)
        sic_path = os.path.join(this_dir, "data", "sec_sic.csv")

        sic = pd.read_csv(sic_path, index_col=0)
        sic = sic.dropna()

        sic_code = sic[sic["ticker"] == self.ticker]["SIC"].values[0]

        return sic_code

    def date_quarter(self, date, q1, q2, q3, q4):
        quarter_list = [(q1, 1), (q2, 2), (q3, 3), (q4, 4)]
        for quarter, quarter_num in quarter_list:
            if self.is_date_between(date, quarter):
                return quarter_num
        return None

    def fiscal_year(self):

        headers = {"Accept": "application/json, text/plain, */*",
                   "Accept-Language": "en-US,en;q=0.9",
                   "Origin": "https://www.nasdaq.com",
                   "Referer": "https://www.nasdaq.com",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

        source = requests.get(url="https://data.sec.gov/submissions/CIK" + self.cik + ".json", headers=headers, verify=True)
        data = source.json()
        end = data["fiscalYearEnd"]
        fiscal_end = datetime.datetime.strptime(end, "%m%d")

        q4 = [fiscal_end + datetime.timedelta(days=-14), fiscal_end + datetime.timedelta(days=14)]
        q1 = [q4[0] + datetime.timedelta(days=76), q4[1] + datetime.timedelta(days=104)]
        q2 = [q1[0] + datetime.timedelta(days=76), q1[1] + datetime.timedelta(days=104)]
        q3 = [q2[0] + datetime.timedelta(days=76), q2[1] + datetime.timedelta(days=104)]

        return q1, q2, q3, q4

    @ratelimit.sleep_and_retry
    @ratelimit.limits(calls = 10, period = 1)
    def SEC(self):
        """
        Function to get a Pandas dataframe from the SEC API of a chosen ticker
        """
        # Defining the headers for access
        headers = {"Accept": "application/json, text/plain, */*",
                   "Accept-Language": "en-US,en;q=0.9",
                   "Origin": "https://www.nasdaq.com",
                   "Referer": "https://www.nasdaq.com",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

        try:
            source = requests.get(url="https://www.sec.gov/files/company_tickers.json", headers=headers, verify=True)
            cik = source.json()

        except:
            this_dir, this_filename = os.path.split(__file__)
            source = os.path.join(this_dir, "data", "company_tickers.json")

            with open(source) as f:
                cik = json.load(f)

        cik = pd.DataFrame(cik)
        cik = cik.transpose()

        value = str(cik.loc[cik["ticker"] == self.ticker]["cik_str"].iloc[0])

        # Making sure the CIK is of right length
        value = value.zfill(10)

        url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK' + value + '.json'

        # Getting the Pandas dataframe of chosen ticker
        source = requests.get(url=url, headers=headers, verify=True)
        data = source.json()
        data = pd.DataFrame(data)
        return data

    def lookup(self, node, year, category, quarter = None):
        """
        Looks up items that are under the "us-gaap" taxonomy and are in USD units, this has to be done year by year or quarter
        by quarter as companies may change what they file certain items under
        """
        item = node.name

        data = self.data

        try:
            data = data["facts"]["ifrs-full"]

        except:
            data = data["facts"]["us-gaap"]

        if (category == "EPS"):
            """
            Creating search term
            """
            try:
                df = pd.DataFrame(pd.DataFrame(data[item])["units"].iloc[0])
                df.dropna(inplace = True)

                df["frame"] = df["frame"].str.replace('CY', '')

                if (quarter != None):
                    # If looking at quarter then:

                    df = df[df["frame"].str.contains(str(year))]

                    unique_quarters = set(df["frame"])
                    all_quarters = [str(year) + "Q" + str(i) for i in range(1, 5)]
                    missing_quarter = list(set(all_quarters) - unique_quarters)

                    if (len(missing_quarter) == 1):
                        df["frame"] = df["frame"].replace(str(year), missing_quarter[0])

                    search = str(year) + "Q" + str(quarter)

                else:
                    search = str(year)

                return df["val"].to_numpy()[df["frame"].to_numpy() == search][0]

            except:
                return False

        if (category == "income"):
            """
            Creating search term
            """
            try:
                df = pd.DataFrame(pd.DataFrame(data[item])["units"].iloc[0])
                df.dropna(inplace = True)
                df["frame"] = df["frame"].str.replace('I', '')

                if (quarter != None):
                    # If looking at quarter then:
                    search = "CY" + str(year) + "Q" + str(quarter)
                else:
                    search = "CY" + str(year)

                return df["val"].to_numpy()[df["frame"].to_numpy() == search][0]

            except:
                return False


        if (category == "balance"):

            """
            Getting the desired item value
            """
            try:

                df = pd.DataFrame((pd.DataFrame(data[item])["units"]).iloc[0])
                df.dropna(inplace = True)
                df["frame"] = df["frame"].str.replace('I', '')
                fy = df[df["fp"] == "FY"].iloc[-1].iloc[7][-2:]

                if (quarter == None):
                    search = "CY" + str(year) + fy
                else:
                    search = "CY" + str(year) + "Q" + str(quarter)

                return df["val"].to_numpy()[df["frame"].to_numpy() == search][0]

            except:

                return False

        if (category == "cashflow"):
            try:
                df = pd.DataFrame((pd.DataFrame(data[item])["units"]).iloc[0])
            except:
                return False

            if (df.shape[1] == 8):
                try:
                    df.drop_duplicates(subset=["end", "val"], inplace=True, keep="last")
                    df['end'] = pd.to_datetime(df["end"], format='%Y-%m-%d')

                    df["year"] = df['end'].dt.year
                    df["quarter"] = df["end"].dt.quarter
                    df["quarter_frame"] = df["year"].astype(str) + "Q" + df["quarter"].astype(str)

                    if (quarter == None):
                        search = str(year) + "Q" + str(4)
                        try:
                            return df["val"].to_numpy()[df["quarter_frame"].to_numpy() == search][0]
                        except:
                            return False
                    else:
                        search = str(year) + "Q" + str(quarter)
                        try:
                            return df["val"].to_numpy()[df["quarter_frame"].to_numpy() == search][0]
                        except:
                            return False
                except:
                    pass

            else:
                df['end'] = pd.to_datetime(df["end"], format='%Y-%m-%d')
                df['start'] = pd.to_datetime(df["start"], format='%Y-%m-%d')
                df.drop_duplicates(subset=['start', "end"], inplace=True, keep="last")

                df["difference_days"] = (df["end"] - df["start"]).dt.days
                df["flag"] = df["difference_days"].between(76, 104)

                df["year"] = df['end'].dt.year
                df["quarter"] = df['end'].dt.quarter
                df["quarter_frame"] = df["year"].astype(str) + "Q" + df["quarter"].astype(str)

                df['frame'] = np.where(df['difference_days'].between(350, 380), df['year'].astype(str), np.nan)
                df.sort_values(['year', 'quarter', "end", "difference_days"], inplace=True)
                df.drop_duplicates(subset=['year', "quarter"], inplace=True, keep="last")

                """
                #Calculating the quarter_vals
                """
                df.loc[~df['flag'], 'quarter_val'] = df.groupby('start')['val'].diff(periods=1)
                df.loc[df['quarter_val'].isnull(), 'quarter_val'] = df['val']
                df["quarter_val"] = df["quarter_val"].astype(np.int64)
                df.reset_index(drop=True, inplace=True)

                if (quarter == None):
                    search = str(year)
                    try:
                        return df["val"].to_numpy()[df["frame"].to_numpy() == search][0]
                    except:
                        return False
                else:
                    search = str(year) + "Q" + str(quarter)
                    try:
                        return df["quarter_val"].to_numpy()[df["quarter_frame"].to_numpy() == search][0]
                    except:
                        return False

    def tree_item(self, node, year, values, attributes, category, quarter = None):
        """
        Returns the value of a chosen node at a certain point in time, using a tree-based node system and summing where needed
        """
        check = self.lookup(node, year, category, quarter)

        if (check != False):
            values.append(check)
            attributes.append(node.attribute)

        else:
            [self.tree_item(i, year, values, attributes, category, quarter) for i in node.getChildrenNodes()]

        # This is done after checking all the nodes
        df = pd.DataFrame(zip(values, attributes), columns=["USD", "Attribute"])

        # Sum credits and subtract credits
        parent_attribute = node.attribute

        if (parent_attribute == "debit"):
            value = df.loc[df["Attribute"] == "debit"]["USD"].sum() - df.loc[df["Attribute"] == "credit"]["USD"].sum()

        else:
            value = df.loc[df["Attribute"] == "credit"]["USD"].sum() - df.loc[df["Attribute"] == "debit"]["USD"].sum()

        return value

    def year_tree_item(self, node, start, end, category, quarter = None):
        """
        Returns a given tree_item over a timeframe
        """
        year_list = [i for i in np.arange(end, start - 1, -1)]
        values = []

        if quarter != None:
            values = [self.tree_item(node, i, [], [], category, j) for i in year_list for j in np.arange(4, 0, -1)]

        else:
            values = [self.tree_item(node, i, [], [], category) for i in year_list]

        return values

    def income(self, start, end, category = "income", quarter = None, readable = None):

        df = self.income_helper(start, end, category, quarter, readable)
        df = df.drop(["Cost and Expenses", "Interest Expense", "Depreciation and Amortization"])

        no_columns = -1*len(df.columns)

        nodes = [s_b,s_d]

        data = [self.year_tree_item(i, start, end, category = "EPS", quarter = True) for i in nodes]

        for i in range(len(data)):
            if no_columns == -1:
                data[i] = data[i][-1]

            else:
                data[i] = data[i][no_columns:]

        df.loc["Number of Basic Shares"] = data[0]
        df.loc["Number of Diluted Shares"] = data[1]
        df.loc["Basic EPS"] = df.loc["Net Profit"]/df.loc["Number of Basic Shares"]
        df.loc["Diluted EPS"] = df.loc["Net Profit"]/df.loc["Number of Diluted Shares"]
        df = df.round(1).map('{:.1f}'.format).replace('\.0$', '', regex=True) # Changed
        df.replace("inf", np.nan, inplace=True)
        return df

    def income_helper(self, start, end, category, quarter = None, readable = None):
        """
        Creating list of years and quarters for columns
        """
        year_list = [i for i in np.arange(end, start - 2, -1)]
        quarter_list = [str(i) + "Q" + str(j) for i in year_list for j in np.arange(4, 0, -1)]

        """
        Creating list of income statement items and their names
        """
        nodes = [rev, cor, gp, opex, ce,
                 oi1,
                 noi, pti1, tax1, ni,
                 cce5_2,
                 ide1_1]
        node_names = ["Revenues", "Cost of Revenue", "Gross Profit", "Operating Expenses", "Cost and Expenses",
                      "Operating Profit"
                     ,"Non-Operating Income/Expense", "Pretax Profit", "Tax", "Net Profit", "Depreciation and Amortization"
                     ,"Interest Expense"]
        """
        Appending each node values for each year to a data
        """
        if quarter == True:
            data = [self.year_tree_item(i, start - 1, end, category, quarter) for i in nodes]
            df = pd.DataFrame(data, index = [node_names], columns = [quarter_list])

            """
            Get the missing quarter stuff, some zeros will be replaced at sense-checking stage, the zeros will signify the quarter that the company reports in
            """
            for i in np.arange(start, end + 1):
                df1 = df.filter(regex=str(i))  # Filtering for only a year i's items
                try:
                    position = [True if self.MissingQuarter(df1, i) > 3 else False for i in df1.columns].index(True)
                    label = df1.columns[position]  # Getting the column name of the label
                    idx = df.columns.get_loc(label)
                    idx_list = [x for x in np.arange(idx, idx + 4)]   # Getting the last four quarters from label backwards by index
                    df1 = df.iloc[:, idx_list]  # Getting the dataframe for the chosen four quarters

                    totals = df1.sum(axis = 1).values  # Summing across income statement items for a given year's quarters
                    """
                    Getting the annual figures for comparison into an "actual" list
                    """
                    if readable == True:
                        annual = [int(x.replace(',', '')) for x in self.income_helper(i, i, category = "income", quarter = False, readable = True)[i]]
                    else:
                        annual = list(self.income_helper(i, i, category = "income", quarter = False, readable = False)[i])

                    changed = list(df.loc[:, label])  # The list of values that are to be changed, i.e. the incorrect column

                    diff = [a - b + c for a, b, c in zip(annual, totals, changed)]  # Reconcile discrepancies and the actual figures
                    df.loc[:, label] = diff

                except:

                    continue

        else:

            data = [self.year_tree_item(i, start - 1, end, category = "income") for i in nodes]
            df = pd.DataFrame(data, index=[node_names], columns=[year_list])

        df.columns = df.columns.get_level_values(0)
        df.index = df.index.get_level_values(0)

        """
        Sense-checking
        """

        df.loc["Cost of Revenue"] = df.loc["Revenues"] - df.loc["Gross Profit"]

        mask = (df.loc["Cost of Revenue"] == 0) & (df.loc["Cost and Expenses"] != 0) & (df.loc["Operating Expenses"] != 0)
        df.loc["Cost of Revenue", mask] = df.loc["Cost and Expenses", mask] - df.loc["Operating Expenses", mask]

        df.loc["Gross Profit"] = df.loc["Revenues"] - df.loc["Cost of Revenue"]

        mask = (df.loc["Operating Profit"] == 0) & (df.loc["Operating Expenses"] != 0) & (df.loc["Gross Profit"] != 0)
        df.loc["Operating Profit", mask] = df.loc["Gross Profit", mask] - df.loc["Operating Expenses", mask]

        df.loc["Operating Expenses"] = df.loc["Gross Profit"] - df.loc["Operating Profit"]
        df.loc["Non-Operating Income/Expense"] = df.loc["Pretax Profit"] - df.loc["Operating Profit"]
        df.loc["EBIT"] = df.loc["Net Profit"] + df.loc["Tax"] + df.loc["Interest Expense"]
        df.loc["EBITDA"] = df.loc["EBIT"] + df.loc["Depreciation and Amortization"]

        if readable == True:
            df = df.applymap(lambda x: '{:,}'.format(x))
            df = df.loc[:, (df != 0).any(axis=0)]
            df.drop(df.filter(regex=str(start - 1)).columns, axis=1, inplace=True)
            return df

        else:
            df = df.loc[:, (df != 0).any(axis=0)] #Remove columns that have all zeros
            df.drop(df.filter(regex=str(start - 1)).columns, axis=1, inplace=True)
            return df

    def MissingQuarter(self, df, column):
        """
        Returns the number of times 0 appears in a column
        """
        try:
            return (df[column].value_counts()[0])
        except:
            return 0

    def cashflow(self, start, end, quarter=None, readable=None, category="cashflow"):
        """
        Creating list of years and quarters for columns
        """
        year_list = [i for i in np.arange(end, start - 1, -1)]
        quarter_list = [str(i) + "Q" + str(j) for i in year_list for j in np.arange(4, 0, -1)]
        """
        Creating list of income statement items and their names
        """
        nodes = [cce2_3, cce2_4, cce2_5, cce1_1, cce1, cce4_8]

        node_names = ["Operating Cash Flow", "Investing Cash Flow", "Financing Cash Flow",
                      "Effect of Exchange Rate on Cash", "End Cash Position", "Capital Expenditures"]
        """
        Appending each node values for each year to a data
        """
        if quarter == True:
            data = [self.year_tree_item(i, start, end, quarter = True, category = "cashflow") for i in nodes]
            df = pd.DataFrame(data, index = [node_names], columns = [quarter_list])

        else:
            data = [self.year_tree_item(i, start, end, category = "cashflow") for i in nodes]
            df = pd.DataFrame(data, index = [node_names], columns = [year_list])

        df.columns = df.columns.get_level_values(0)
        df.index = df.index.get_level_values(0)

        df.loc["Free Cash Flow"] = df.loc["Operating Cash Flow"] - df.loc["Capital Expenditures"]
        df.drop(["Capital Expenditures"], inplace=True)
        df = df.loc[:, (df != 0).any(axis=0)]

        if readable == True:
            df = df.applymap(lambda x: '{:,}'.format(x))
            return df
        else:
            return df

    def balance(self, start, end, quarter = None, readable = None):
        """
        Creating list of years and quarters for columns
        """
        year_list = [i for i in np.arange(end, start - 1, -1)]
        quarter_list = [str(i) + "Q" + str(j) for i in year_list for j in np.arange(4, 0, -1)]

        """
        Getting SIC code
        """

        sic_code = self.SIC

        bank_codes = [6022, 6021, 6211, 6029, 6035, 6199]

        if sic_code in bank_codes:
            nodes = [ca1_1, ba1_1, ba1_4,
                     ba1_6, ba1_7, ba1_9, ba1_15, ba1_3, ba1_18,
                     ba1_10, nca1_19, ba1_16, ba1_11, a,
                     bl1_1, bl1_3, bl1_9,
                     cl1_3, bl1_6,
                     bl1_8, bl1_10, l,
                     se2_3, se2_8, se2_12, se2_11,
                     se1_1, se1_2, se]

            node_names = ["Cash and Cash Equivalents", "Securities Purchased Under Agreements to Resell", "Net Loans",
                          "Trading Securities", "Available-For-Sale Securities","Held-To-Maturity Securities", "Derivative Securities", "Securities Borrowed", "Financial Instruments Owned",
                          "Property, Plant and Equipment", "Intangibles", "Accounts Receivables", "Other Assets", "Total Assets",
                          "Securities Sold Under Agreements to Repurchase","Deposits", "Short Sales Obligations",
                          "Short-Term Debt", "Long-Term Debt",
                          "Accrued Expenses and Accounts Payable", "Other Liabilities", "Total Liabilities",
                          "Common Stock", "Additional Paid In Capital", "Retained Earnings", "Accumulated Other Income",
                          "Stockholder's Equity", "Minority Interest", "Total Equity"]


        else:
            nodes = [ca1_1, ca1_4, ca2_12,
                     ca1_34, ca1,
                     nca1_13, nca1_19, nca1_36,
                     nca,
                     cl2_1, cl2_2, cl1_2, cl1_3,
                     cl1_27, cl1,
                     ncl1_1, ncl1_2, ncl,
                     se2_3, se2_8, se2_12, se2_14,
                     se1_1, se1_2,
                     a, l, se]

            node_names = ["Cash and Cash Equivalents", "Accounts Receivable, Net", "Inventories",
                          "Other Current Assets", "Total Current Assets",
                          "Property Plant and Equipment", "Intangibles", "Other Non-Current Assets",
                          "Total Non-Current Assets",
                          "Accounts Payable", "Accrued Liabilities", "Deferred Revenue", "Short-term Borrowings",
                          "Other Current Liabilities", "Total Current Liabilities",
                          "Long-Term Debt", "Non-Debt Long Term Liabilities", "Total Non-Current Liabilities",
                          "Capital Stock", "Additional Paid In Capital", "Retained Earnings", "Accumulated Other Change",
                          "Stockholder's Equity", "Minority Interest",
                          "Total Assets", "Total Liabilities", "Total Equity"]

        """
        Appending each node values for each year to a data
        """
        if quarter == True:
            data = [self.year_tree_item(i, start, end, category = "balance", quarter=True) for i in nodes]  # Fetching the data
            df = pd.DataFrame(data, index=[node_names], columns=[quarter_list])  # Creating the dataframe with columns and index according to the list

        else:
            data = [self.year_tree_item(i, start, end, category = "balance") for i in nodes]
            df = pd.DataFrame(data, index=[node_names], columns=[year_list])

        df.columns = df.columns.get_level_values(0)
        df.index = df.index.get_level_values(0)

        """
        Sense-checking
        """
        if sic_code not in bank_codes:
            df.loc["Total Non-Current Assets"] = df.loc["Total Assets"] - df.loc["Total Current Assets"]
            df.loc["Other Current Assets"] = df.loc["Total Current Assets"] - df.iloc[0:3].sum()
            df.loc["Other Non-Current Assets"] = df.loc["Total Non-Current Assets"] - df.iloc[5:7].sum()

            df.loc["Other Current Liabilities"] = df.loc["Total Current Liabilities"] - df.iloc[9:13].sum()
            df.loc["Total Non-Current Liabilities"] = df.loc["Total Liabilities"] - df.loc["Total Current Liabilities"]
            df.loc["Non-Debt Long Term Liabilities"] = df.loc["Total Non-Current Liabilities"] - df.loc["Long-Term Debt"]

            df.loc["Accumulated Other Change"] = df.loc["Stockholder's Equity"] - df.iloc[18:21].sum()
            df.loc["Minority Interest"] = df.loc["Total Equity"] - df.loc["Stockholder's Equity"]

        else:

            df.loc["Other Assets"] = df.loc["Total Assets"] - df.iloc[0:12].sum()
            df.loc["Other Liabilities"] = df.loc["Total Liabilities"] - df.iloc[14:20].sum()

        if readable == True:

            df = df.applymap(lambda x: '{:,}'.format(x))
            df = df.loc[:, (df != 0).any(axis=0)]
            return df

        else:

            df = df.loc[:, (df != 0).any(axis=0)]
            return df

    def comparables(self, n, level = None):
        this_dir, this_filename = os.path.split(__file__)
        sic_path = os.path.join(this_dir, "data", "sec_sic.csv")

        if level == None:
            level = 4

        sic = pd.read_csv(sic_path, index_col=0)
        sic = sic.dropna()

        sic["SIC"] = sic["SIC"].astype(int)
        sic["SIC"] = sic["SIC"].astype(str)
        sic['SIC'] = sic['SIC'].apply(lambda x: x[:level])
        sic["SIC"] = sic["SIC"].astype(int)

        sic_code = sic[sic["ticker"] == self.ticker]["SIC"].values[0]
        company_list = sic[sic["SIC"] == sic_code].copy()
        company_list.drop(["cik_str"], axis=1, inplace=True)
        company_list.reset_index(drop=True, inplace=True)

        sic_index = company_list[company_list['ticker'] == self.ticker].index[0]  # Getting index of desired row

        n_above = n // 2
        n_below = n - n_above

        start_row = max(0, sic_index - n_above)  # Getting the index
        end_row = min(sic_index + n_below, len(company_list) - 1)

        surronding_companies = company_list.iloc[start_row:end_row + 1]

        if len(surronding_companies) < (n + 1):
            n_below = n - len(surronding_companies) + 1
            end_row = min(end_row + n_below, len(company_list) - 1)
            surronding_companies = company_list.iloc[start_row:end_row + 1]

        if len(surronding_companies) < (n + 1):
            n_above = n - len(surronding_companies) + 1
            start_row = max(0, start_row - n_above)
            surronding_companies = company_list.iloc[start_row:end_row + 1]

        surronding_companies = surronding_companies.rename(columns={'ticker': 'Ticker', 'title': 'Name'})

        return surronding_companies

    def ratios(self, start, end):

        df = self.data
        df = df["facts"]
        sic_code = self.SIC
        bank_codes = [6022, 6021, 6211, 6029, 6035, 6199]

        balance_r = self.balance(start - 1, end)
        income_r = self.income(start, end).astype(float)
        cash_r = self.cashflow(start, end)

        year_list = [i for i in np.arange(end, start - 1, -1)]

        try:
            cap_df = pd.DataFrame(df["dei"]["EntityPublicFloat"]["units"]["USD"])
            cap_df["fy"] = cap_df["frame"].str[2:6]
        except:
            next

        cap = []
        for i in year_list:
            try:
                cap.append(cap_df.loc[cap_df['fy'] == str(i), 'val'].iloc[0])
            except:
                cap.append(None)

        cap = pd.Series(cap, index=year_list)

        ebitda = income_r.loc["EBITDA"]
        ebit = income_r.loc["EBIT"]
        net_profit = income_r.loc["Net Profit"]
        operating_profit = income_r.loc["Operating Profit"]
        tax = income_r.loc["Tax"]

        if sic_code in bank_codes:
            total_assets = balance_r.loc["Total Assets"]
            total_liabilities = balance_r.loc["Total Liabilities"]
            total_se = balance_r.loc["Stockholder's Equity"]
            total_equity = balance_r.loc["Total Equity"]
            cash = balance_r.loc["Cash and Cash Equivalents"]

        else:
            current_assets = balance_r.loc["Total Current Assets"]
            total_assets = balance_r.loc["Total Assets"]
            current_liabilities = balance_r.loc["Total Current Liabilities"]
            total_liabilities = balance_r.loc["Total Liabilities"]
            total_se = balance_r.loc["Stockholder's Equity"]
            total_equity = balance_r.loc["Total Equity"]
            inventory = balance_r.loc["Inventories"]
            cash = balance_r.loc["Cash and Cash Equivalents"]
            nwc = (current_assets - current_liabilities).diff(-1)

        fcf = cash_r.loc["Free Cash Flow"]

        d_a = pd.Series(self.year_tree_item(cce5_2, start, end, "income"), index=year_list)
        capex = pd.Series(self.year_tree_item(cce4_8, start, end, "cashflow"), index=year_list)

        if sic_code in bank_codes:
            ufcf = operating_profit + tax - capex + d_a
        else:
            ufcf = operating_profit + tax - capex + d_a - nwc

        cap = cap + total_liabilities - cash

        ratio_df = pd.DataFrame(columns=year_list)

        if sic_code in bank_codes:
            ratio_df.loc["Debt-to-Equity Ratio"] = (total_liabilities / total_se)

            ratio_df.loc["Return on Equity"] = (net_profit / total_se)
            ratio_df.loc["Return on Assets"] = (net_profit / total_assets)
            ratio_df.loc["Return on Invested Capital"] = (operating_profit + tax) / (total_liabilities + total_equity)

            ratio_df.loc["FCFF Yield"] = ufcf / (cap)

            ratio_df.loc["EV/EBITDA"] = (cap / ebitda)

        else:
            ratio_df.loc["Current Ratio"] = (current_assets / current_liabilities)
            ratio_df.loc["Quick Ratio"] = ((current_assets - inventory) / current_liabilities)

            ratio_df.loc["Debt-to-Equity Ratio"] = (total_liabilities / total_se)

            ratio_df.loc["Return on Equity"] = (net_profit / total_se)
            ratio_df.loc["Return on Assets"] = (net_profit / total_assets)
            ratio_df.loc["Return on Capital Employed"] = ebit / (total_assets - current_liabilities)
            ratio_df.loc["Return on Invested Capital"] = (operating_profit + tax) / (total_liabilities + total_equity)

            ratio_df.loc["FCFF Yield"] = ufcf / (cap)

            ratio_df.loc["EV/EBITDA"] = (cap / ebitda)

        ratio_df.dropna(axis=1, how='all', inplace=True)

        ratio_df["Mean"] = ratio_df.mean(axis=1)

        return ratio_df

"""
Banks and financial services balance sheet items
"""

#ca3_1 # Cash due from banks
#ca3_2 # Deposits from other banks

"""
Banks - Assets
"""

#Level 1
ba1_1 = Node("FederalFundsSoldAndSecuritiesPurchasedUnderAgreementsToResell", attribute = "debit") #Securities Purchased Under Agreements to Resell
ba1_12 = Node("CarryingValueOfFederalFundsSoldSecuritiesPurchasedUnderAgreementsToResellAndDepositsPaidForSecuritiesBorrowed", attribute = "debit", parent = ba1_1)
ba1_13 = Node("CarryingValueOfSecuritiesPurchasedUnderAgreementsToResellAndDepositsPaidForSecuritiesBorrowed", attribute = "debit", parent = ba1_12)



ba1_4 = Node("NotesReceivableNet", attribute = "debit") #Loans and Leases, Net
ba1_5 = Node("FinancingReceivableExcludingAccruedInterestAfterAllowanceForCreditLoss", attribute = "debit", parent = ba1_4) #Loans and Leases

ba1_3 = Node("SecuritiesBorrowed", attribute = "debit") # Securities Borrowed

ba1_14 = Node("MarketableSecurities", attribute = "debit") #Marketable Securities

ba1_6 = Node("TradingSecurities", attribute = "debit", parent = ba1_14) #Trading Securities

ba1_15 = Node("DerivativeAssets", attribute = "debit", parent = ba1_14) #Derivative Assets
ba1_15_1 = Node("DerivativeFinancialAssets", attribute = "debit", parent = ba1_15) #Derivative Assets

ba1_7 = Node("AvailableForSaleSecuritiesDebtSecurities", attribute = "debit", parent = ba1_14) #Available-For-Sale Securities
ba1_8 = Node("DebtSecuritiesAvailableForSaleExcludingAccruedInterest", attribute = "debit", parent = ba1_7) #Available-For-Sale Securities

ba1_9 = Node("DebtSecuritiesHeldToMaturityExcludingAccruedInterestAfterAllowanceForCreditLoss", attribute = "debit", parent = ba1_14) #Held-To-Maturity Securities
ba1_17 = Node("DebtSecuritiesHeldToMaturityAmortizedCostAfterAllowanceForCreditLoss", attribute = "debit", parent = ba1_9)

ba1_10 = Node("PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization", attribute = "debit") #Premises and Equipment

ba1_11 = Node("OtherAssets", attribute = "debit")

ba1_16 = Node("AccountsReceivableNet", attribute = "debit") # Accounts Receivables

ba1_18 = Node("FinancialInstrumentsOwnedAtFairValue", attribute = "debit") #Financial Instruments Owned

#Level 2
ba2_22 = Node("LoansAndAdvancesToCustomers", attribute = "debit", parent = ba1_4)
ba2_23 = Node("LoansAndAdvancesToBanks", attribute = "debit", parent = ba1_4)
ba2_24 = Node("CorporateLoans", attribute = "debit", parent = ba2_22)
ba2_25 = Node("ConsumerLoans", attribute = "debit", parent = ba2_22)
ba2_26 = Node("LoansToGovernment", attribute = "debit", parent = ba2_22)


ba2_1 = Node("FederalFundsSold", attribute = "debit", parent = ba1_13)
ba2_2 = Node("SecuritiesPurchasedUnderAgreementsToResell", attribute = "debit", parent = ba1_13)

ba2_3 = Node("FinancingReceivableAllowanceForCreditLossExcludingAccruedInterest", attribute = "credit", parent = ba1_5)
ba2_4 = Node("FinancingReceivableAllowanceForCreditLosses", attribute = "credit", parent = ba2_3)

ba2_5 = Node("FinancingReceivableExcludingAccruedInterestBeforeAllowanceForCreditLoss", attribute = "debit", parent = ba1_5)
ba2_6 = Node("NotesReceivableGross", attribute = "debit", parent = ba2_5) # Gross loans

ba2_7 = Node("TradingSecuritiesDebt", attribute = "debit", parent = ba1_6)
ba2_8 = Node("EquitySecuritiesFvNiCurrentAndNoncurrent", attribute = "debit", parent = ba1_6)

ba2_9 = Node("DebtSecuritiesHeldToMaturityAllowanceForCreditLossExcludingAccruedInterest", attribute = "credit", parent = ba1_17)
ba2_22 = Node("DebtSecuritiesHeldToMaturityAllowanceForCreditLoss", attribute = "credit", parent = ba2_9)
ba2_10 = Node("DebtSecuritiesHeldToMaturityExcludingAccruedInterestBeforeAllowanceForCreditLoss", attribute = "debit", parent = ba1_17)
ba2_21 = Node("HeldToMaturitySecurities", attribute = "debit", parent = ba2_10)

ba2_11 = Node("FinanceLeaseRightOfUseAsset", attribute = "credit", parent = ba1_10)
ba2_12 = Node("PropertyPlantAndEquipmentNet", attribute = "debit", parent = ba1_10)
ba2_12_1 = Node("PropertyPlantAndEquipment", attribute = "debit", parent = ba2_12)

ba2_13 = Node("ReceivablesFromCustomers", attribute = "debit", parent = ba1_16)
ba2_20 = Node("ContractWithCustomerReceivableAfterAllowanceForCreditLossCurrent", attribute = "debit", parent = ba2_13)
ba2_14 = Node("ReceivablesFromBrokersDealersAndClearingOrganizations", attribute = "debit", parent = ba1_16)
ba2_15 = Node("AccountsReceivableFromSecuritization", attribute = "debit", parent = ba1_16)
ba2_16 = Node("AccountsReceivableBilledForLongTermContractsOrPrograms", attribute = "debit", parent = ba1_16)
ba2_17 = Node("NotesReceivableGross", attribute = "debit", parent = ba1_16)
ba2_18 = Node("AccruedInvestmentIncomeReceivable", attribute = "debit", parent = ba1_16)
ba2_19 = Node("PremiumsReceivableAtCarryingValue", attribute = "debit", parent = ba1_16)
ba2_20 = Node("OtherReceivables", attribute = "debit", parent = ba1_16)
ba2_30 = Node("TradeAndOtherReceivablesDueFromRelatedParties", attribute = "debit", parent = ba1_16)
ba2_31 = Node("TradeReceivables", attribute = "debit", parent = ba1_16)

ba2_32 = Node("FinancialAssets", attribute = "debit", parent = ba1_18)
"""
Banks - Liabilities
"""
#Level 1
bl1_1 = Node("FederalFundsPurchasedAndSecuritiesSoldUnderAgreementsToRepurchase", attribute = "credit") #Securities Loaned
bl1_2 = Node("CarryingValueOfSecuritiesSoldUnderRepurchaseAgreementsAndDepositsReceivedForSecuritiesLoaned", attribute = "credit", parent = bl1_1)

bl1_3 = Node("Deposits", attribute = "credit") #Total Deposits

bl1_4 = Node("TradingLiabilities", attribute = "credit") #Trading Liabilities

bl1_5 = Node("ShortTermBorrowings", attribute = "credit") #Short-Term Debt

bl1_6 = Node("LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities", attribute = "credit") #Long-Term Debt

bl1_8 = Node("AccountsPayableAndAccruedLiabilitiesCurrentAndNoncurrent", attribute = "credit") # Accounts Payable and Accrued Liabilities

bl1_9 = Node("FinancialInstrumentsSoldNotYetPurchasedAtFairValue", attribute = "credit") # Short-sales

bl1_10 = Node("Other", attribute = "credit")

#Level 2
bl2_1 = Node("FederalFundsPurchased", attribute = "credit", parent = bl1_2)
bl2_2 = Node("SecuritiesSoldUnderAgreementsToRepurchase", attribute = "credit", parent = bl1_2)

bl2_3 = Node("LongTermDebt", attribute = "credit", parent = bl1_6)

bl2_4 = Node("AccountsPayableCurrentAndNoncurrent", attribute = "credit", parent = bl1_8)
bl2_5 = Node("AccruedLiabilitiesCurrentAndNoncurrent", attribute = "credit", parent = bl1_8)

bl2_6 = Node("DepositsFromBanks", attribute = "credit", parent = bl1_3)
bl2_7 = Node("DepositsFromCustomers", attribute = "credit", parent = bl1_3)

#Level 3


bl3_1 = Node("AccruedLiabilitiesAndOtherLiabilities", attribute = "credit", parent = bl2_5)
bl3_2 = Node("EmployeeRelatedLiabilitiesCurrentAndNoncurrent", attribute = "credit", parent = bl2_5)
bl3_3 = Node("OtherAccruedLiabilitiesCurrentAndNoncurrent", attribute = "credit", parent = bl2_5)

bl3_4 = Node("PayablesToCustomers", attribute = "credit", parent = bl2_4)
bl3_5 = Node("AccountsPayableTradeCurrentAndNoncurrent", attribute = "credit", parent = bl2_4)
bl3_6 = Node("AccountsPayableInterestBearingCurrentAndNoncurrent", attribute = "credit", parent = bl2_4)

#Level 4

bl4_1 = Node("AccruedEmployeeBenefitsCurrentAndNoncurrent", attribute = "credit", parent = bl3_2)
bl4_2 = Node("AccruedSalariesCurrentAndNoncurrent", attribute = "credit", parent = bl3_2)
bl4_3 = Node("WorkersCompensationLiabilityCurrentAndNoncurrent", attribute = "credit", parent = bl3_2)
bl4_4 = Node("OtherEmployeeRelatedLiabilitiesCurrentAndNoncurrent", attribute = "credit", parent = bl3_2)

"""
No. of shares
"""
s_b = Node("WeightedAverageNumberOfSharesOutstandingBasic", attribute = "debit")
s_d = Node("WeightedAverageNumberOfDilutedSharesOutstanding", attribute = "debit")

s_b1 = Node("WeightedAverageShares", attribute = "debit", parent = s_b)
s_d1 = Node("AdjustedWeightedAverageShares", attribute = "debit", parent = s_d)
"""
EPS
"""

eps = Node("EarningsPerShareBasic", attribute = "credit")
eps_d = Node("EarningsPerShareDiluted", attribute = "credit")

eps1 = Node("BasicEarningsLossPerShare", attribute = "credit", parent = eps)
eps_d1 = Node("DilutedEarningsLossPerShare", attribute = "credit", parent = eps_d)
"""
Net Income
"""

ni = Node("NetIncomeLoss", attribute="credit")

# Level 1
ni1_1 = Node("ProfitLoss", attribute="credit", parent=ni)

"""
Pre-tax income
"""
pti1 = Node("ProfitLossBeforeTax", attribute="credit", parent=ni1_1) # IFRS
pti = Node("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", attribute="credit", parent=pti1)

# Level 1

pti1_1 = Node("IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", attribute="credit", parent=pti)

"""
Tax
"""
tax1 = Node("IncomeTaxExpenseContinuingOperations", attribute="debit", parent=ni1_1) #IFRS
tax = Node("IncomeTaxExpenseBenefit", attribute="debit", parent=tax1)

"""
Operating Income
"""
oi1 = Node("ProfitLossFromOperatingActivities", attribute="credit", parent=pti1_1) #IFRS
oi = Node("OperatingIncomeLoss", attribute="credit", parent=oi1)

"""
Gross Profit
"""
# Level 1
gp = Node("GrossProfit", attribute="credit", parent=oi)

"""
Revenue
"""
rev = Node("Revenues", attribute="credit", parent=gp)

# Level 1

rev1_1 = Node("RevenueFromContractWithCustomerExcludingAssessedTax", attribute="credit", parent=rev)
rev1_2 = Node("RevenueFromContractWithCustomerIncludingAssessedTax", attribute="credit", parent=rev1_1)

rev1_3 = Node("SalesRevenueNet", attribute="credit", parent=rev1_2)
rev1_4 = Node("SalesRevenueGoodsNet", attribute="credit", parent=rev1_3)

rev1_5 = Node("RegulatedAndUnregulatedOperatingRevenue", attribute="credit", parent=rev1_4)

rev1_6 = Node("RevenuesNetOfInterestExpense", attribute="credit", parent=rev1_5)

rev1_7 = Node("Revenue", attribute = "credit", parent = rev1_6) #IFRS

# Level 2

rev2_1 = Node("NoninterestIncome", attribute="credit", parent=rev1_7)
rev2_2 = Node("InterestIncomeExpenseNet", attribute="credit", parent=rev1_7)

"""
Cost of Revenue
"""
cor = Node("CostOfSales", attribute="debit", parent=gp)
cor1 = Node("CostOfRevenue", attribute="debit", parent=cor)

# Level 1
cor1_1 = Node("CostOfGoodsAndServicesSold", attribute="debit", parent=cor)
cor1_2 = Node("FinancingInterestExpense", attribute="debit", parent=cor)
cor1_3 = Node("ProvisionForLoanLeaseAndOtherLosses", attribute="debit", parent=cor)
cor1_4 = Node("PolicyholderBenefitsAndClaimsIncurredNet", attribute="debit", parent=cor)
cor1_5 = Node("LiabilityForFuturePolicyBenefitsPeriodExpense", attribute="debit", parent=cor)
cor1_6 = Node("InterestCreditedToPolicyholdersAccountBalances", attribute="debit", parent=cor)
cor1_7 = Node("PolicyholderDividends", attribute="debit", parent=cor)
cor1_8 = Node("DeferredSalesInducementsAmortizationExpense", attribute="debit", parent=cor)
cor1_9 = Node("PresentValueOfFutureInsuranceProfitsAmortizationExpense1", attribute="debit", parent=cor)
cor1_10 = Node("AmortizationOfMortgageServicingRightsMSRs", attribute="debit", parent=cor)
cor1_11 = Node("DeferredPolicyAcquisitionCostAmortizationExpense", attribute="debit", parent=cor)
cor1_12 = Node("AmortizationOfValueOfBusinessAcquiredVOBA", attribute="debit", parent=cor)
cor1_13 = Node("OtherCostOfOperatingRevenue", attribute="debit", parent=cor)
cor1_14 = Node("MerchantMarineOperatingDifferentialSubsidy", attribute="debit", parent=cor)

# Level 2
cor2_1 = Node("CostDepreciationAmortizationAndDepletion", attribute="debit", parent=cor1_1)
cor2_2 = Node("CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization", attribute="debit", parent=cor1_1)

cor2_3 = Node("ProvisionForOtherCreditLosses", attribute="debit", parent=cor1_3)
cor2_4 = Node("ProvisionForOtherLosses", attribute="debit", parent=cor1_3)
cor2_5 = Node("ProvisionForLoanLossesExpensed", attribute="debit", parent=cor1_3)
cor2_6 = Node("NetInvestmentInLeaseCreditLossExpenseReversal", attribute="debit", parent=cor1_3)

cor2_7 = Node("PolicyholderBenefitsAndClaimsIncurredGross", attribute="debit", parent=cor1_7)

# Level 3
cor3_1 = Node("CostDirectMaterial", attribute="debit", parent=cor2_1)
cor3_2 = Node("CostOfGoodsSoldSalesTypeLease", attribute="debit", parent=cor2_1)
cor3_3 = Node("CostOfGoodsSoldDirectFinancingLease", attribute="debit", parent=cor2_1)
cor3_4 = Node("DirectCostsOfLeasedAndRentedPropertyOrEquipment", attribute="debit", parent=cor2_1)
cor3_5 = Node("CostDirectLabor", attribute="debit", parent=cor2_1)
cor3_6 = Node("CostOfGoodsAndServicesSoldOverhead", attribute="debit", parent=cor2_1)
cor3_7 = Node("CostMaintenance", attribute="debit", parent=cor2_1)
cor3_8 = Node("DirectTaxesAndLicensesCosts", attribute="debit", parent=cor2_1)
cor3_9 = Node("CostOfTrustAssetsSoldToPayExpenses", attribute="debit", parent=cor2_1)
cor3_10 = Node("CostOfPropertyRepairsAndMaintenance", attribute="debit", parent=cor2_1)
cor3_11 = Node("CostOfOtherPropertyOperatingExpense", attribute="debit", parent=cor2_1)
cor3_12 = Node("DirectOperatingCosts", attribute="debit", parent=cor2_1)
cor3_13 = Node("LossOnContracts", attribute="debit", parent=cor2_1)
cor3_14 = Node("AffiliateCosts", attribute="debit", parent=cor2_1)
cor3_15 = Node("InventoryFirmPurchaseCommitmentLoss", attribute="debit", parent=cor2_1)
cor3_16 = Node("ExciseAndSalesTaxes", attribute="debit", parent=cor2_1)
cor3_17 = Node("ProductionRelatedImpairmentsOrCharges", attribute="debit", parent=cor2_1)

cor3_18 = Node("CostOfGoodsAndServicesSoldDepreciationAndAmortization", attribute="debit", parent=cor2_2)
cor3_19 = Node("CostDepletion", attribute="debit", parent=cor2_2)

cor3_18 = Node("PolicyholderBenefitsAndClaimsIncurredGross", attribute="debit", parent=cor2_7)
cor3_19 = Node("ReinsuranceCostsAndRecoveriesNet", attribute="debit", parent=cor2_7)

# Level 4
cor4_1 = Node("CostOfGoodsAndServicesSoldDepreciation", attribute="debit", parent=cor3_18)
cor4_2 = Node("CostOfGoodsAndServicesSoldAmortization", attribute="debit", parent=cor3_18)

cor4_3 = Node("WaterProductionCosts", attribute="debit", parent=cor3_12)
cor4_4 = Node("CostOfPurchasedWater", attribute="debit", parent=cor3_12)
cor4_5 = Node("RecoveryOfDirectCosts", attribute="credit", parent=cor3_12)
cor4_6 = Node("ManufacturingCosts", attribute="debit", parent=cor3_12)
cor4_7 = Node("DirectOperatingMaintenanceSuppliesCosts", attribute="debit", parent=cor3_12)
cor4_8 = Node("OperatingInsuranceAndClaimsCostsProduction", attribute="debit", parent=cor3_12)
cor4_9 = Node("FuelCosts", attribute="debit", parent=cor3_12)
cor4_10 = Node("DirectCommunicationsAndUtilitiesCosts", attribute="debit", parent=cor3_12)
cor4_11 = Node("AircraftRentalAndLandingFees", attribute="debit", parent=cor3_12)
cor4_12 = Node("AircraftMaintenanceMaterialsAndRepairs", attribute="debit", parent=cor3_12)

# Level 5
cor5_1 = Node("DirectOperatingCommunicationsCosts", attribute="debit", parent=cor4_10)

cor5_2 = Node("AircraftRental", attribute="debit", parent=cor4_11)
cor5_3 = Node("LandingFeesAndOtherRentals", attribute="debit", parent=cor4_11)

"""
Operating Expenses
"""
opex1 = Node("NoninterestExpense", attribute = "debit", parent = oi)
opex2 = Node("OperatingExpense", attribute="debit", parent=opex1)
opex = Node("OperatingExpenses", attribute="debit", parent=opex2)

# Level 1
opex1_1 = Node("OperatingCostsAndExpenses", attribute="debit", parent=opex)
opex1_2 = Node("SellingGeneralAndAdministrativeExpense", attribute="debit", parent=opex)
opex1_3 = Node("ProvisionForDoubtfulAccounts", attribute="debit", parent=opex)
opex1_4 = Node("OtherGeneralExpense", attribute="debit", parent=opex)
opex1_5 = Node("GainLossOnDispositionOfAssets1", attribute="debit", parent=opex)
opex1_6 = Node("SalesTypeLeaseSellingProfitLoss", attribute="debit", parent=opex)
opex1_7 = Node("DirectFinancingLeaseSellingLoss", attribute="debit", parent=opex)
opex1_8 = Node("OtherUnderwritingExpense", attribute="debit", parent=opex)
opex1_9 = Node("DemutualizationCostAndExpense", attribute="debit", parent=opex)
opex1_10 = Node("InsuranceCommissions", attribute="debit", parent=opex)
opex1_11 = Node("FloorBrokerageExchangeAndClearanceFees", attribute="debit", parent=opex)
opex1_12 = Node("AdministrativeFeesExpense", attribute="debit", parent=opex)
opex1_13 = Node("IncentiveFeeExpense", attribute="debit", parent=opex)
opex1_14 = Node("ManagementFeeExpense", attribute="debit", parent=opex)

# Level 2
opex2_1 = Node("ResearchAndDevelopmentExpense", attribute="debit", parent=opex1_1)
opex2_2 = Node("DepreciationAndAmortization", attribute="debit", parent=opex1_1)
opex2_3 = Node("ExplorationExpense", attribute="debit", parent=opex1_1)
opex2_4 = Node("CarryingCostsPropertyAndExplorationRights", attribute="debit", parent=opex1_1)
opex2_5 = Node("RecapitalizationCosts", attribute="debit", parent=opex1_1)
opex2_6 = Node("RestructuringSettlementAndImpairmentProvisions", attribute="debit", parent=opex1_1)
opex2_7 = Node("CustodyFees", attribute="debit", parent=opex1_1)
opex2_8 = Node("TrusteeFees", attribute="debit", parent=opex1_1)
opex2_9 = Node("SponsorFees", attribute="debit", parent=opex1_1)
opex2_10 = Node("RoyaltyExpense", attribute="debit", parent=opex1_1)
opex2_11 = Node("AccretionExpenseIncludingAssetRetirementObligations", attribute="debit", parent=opex1_1)
opex2_12 = Node("LoanPortfolioExpense", attribute="debit", parent=opex1_1)
opex2_13 = Node("PreOpeningCosts", attribute="debit", parent=opex1_1)
opex2_14 = Node("GainLossRelatedToLitigationSettlement", attribute="credit", parent=opex1_1)
opex2_15 = Node("MalpracticeLossContingencyClaimsIncurredNet", attribute="debit", parent=opex1_1)
opex2_16 = Node("InsuranceRecoveries", attribute="credit", parent=opex1_1)
opex2_17 = Node("OtherCostAndExpenseOperating", attribute="debit", parent=opex1_1)
opex2_18 = Node("BusinessCombinationIntegrationRelatedCosts", attribute="debit", parent=opex1_1)
opex2_19 = Node("UnsolicitedTenderOfferCosts", attribute="debit", parent=opex1_1)
opex2_20 = Node("ProfessionalAndContractServicesExpense", attribute="debit", parent=opex1_1)

opex2_21 = Node("SellingAndMarketingExpense", attribute="debit", parent=opex1_2)
opex2_22 = Node("GeneralAndAdministrativeExpense", attribute="debit", parent=opex1_2)
opex2_23 = Node("OtherSellingGeneralAndAdministrativeExpense", attribute="debit", parent=opex1_2)

opex2_24 = Node("GainLossOnSaleOfPropertyPlantEquipment", attribute="debit", parent=opex1_5)
opex2_25 = Node("GainLossOnSaleOfBusiness", attribute="debit", parent=opex1_5)
opex2_26 = Node("SaleAndLeasebackTransactionGainLossNet", attribute="debit", parent=opex1_5)
opex2_27 = Node("GainLossOnDispositionOfIntangibleAssets", attribute="debit", parent=opex1_5)
opex2_28 = Node("GainLossOnTerminationOfLease", attribute="debit", parent=opex1_5)
opex2_29 = Node("GainLossOnSaleOfOtherAssets", attribute="debit", parent=opex1_5)

opex2_30 = Node("FloorBrokerage", attribute="debit", parent=opex1_11)
opex2_31 = Node("ExchangeFees", attribute="debit", parent=opex1_11)
opex2_32 = Node("OrderFlowFees", attribute="debit", parent=opex1_11)
opex2_33 = Node("ClearanceFees", attribute="debit", parent=opex1_11)

# Level 3

opex3_1 = Node("ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost", attribute="debit", parent=opex2_1)
opex3_2 = Node("ResearchAndDevelopmentExpenseSoftwareExcludingAcquiredInProcessCost", attribute="debit", parent=opex2_1)
opex3_3 = Node("ResearchAndDevelopmentAssetAcquiredOtherThanThroughBusinessCombinationWrittenOff", attribute="debit", parent=opex2_1)

opex3_4 = Node("DepreciationNonproduction", attribute="debit", parent=opex2_2)
opex3_5 = Node("DepletionOfOilAndGasProperties", attribute="debit", parent=opex2_2)
opex3_6 = Node("AmortizationOfDeferredCharges", attribute="debit", parent=opex2_2)
opex3_7 = Node("OtherDepreciationAndAmortization", attribute="debit", parent=opex2_2)

opex3_8 = Node("RestructuringCharges", attribute="debit", parent=opex2_6)
opex3_9 = Node("BusinessCombinationAcquisitionRelatedCosts", attribute="debit", parent=opex2_6)
opex3_10 = Node("DefinedBenefitPlanRecognizedNetGainLossDueToSettlements1", attribute="debit", parent=opex2_6)
opex3_11 = Node("InventoryRecallExpense", attribute="debit", parent=opex2_6)
opex3_12 = Node("GainOnBusinessInterruptionInsuranceRecovery", attribute="debit", parent=opex2_6)
opex3_13 = Node("EnvironmentalRemediationExpenseAfterRecovery", attribute="debit", parent=opex2_6)
opex3_14 = Node("AssetImpairmentCharges", attribute="debit", parent=opex2_6)

opex3_15 = Node("AssetRetirementObligationAccretionExpense", attribute="debit", parent=opex2_11)
opex3_16 = Node("AccretionExpense", attribute="debit", parent=opex2_11)

opex3_17 = Node("LitigationSettlementAmountAwardedToOtherParty", attribute="credit", parent=opex2_14)
opex3_18 = Node("LitigationSettlementAmountAwardedFromOtherParty", attribute="debit", parent=opex2_14)
opex3_19 = Node("LitigationSettlementInterest", attribute="debit", parent=opex2_14)
opex3_20 = Node("LitigationSettlementExpense", attribute="debit", parent=opex2_14)

opex3_21 = Node("MalpracticeLossContingencyClaimsIncurredInPeriod", attribute="debit", parent=opex2_15)
opex3_22 = Node("MalpracticeLossContingencyReturnOfPremiums", attribute="credit", parent=opex2_15)
opex3_23 = Node("MalpracticeLossContingencyInsuranceRecoveries", attribute="credit", parent=opex2_15)
opex3_24 = Node("MalpracticeLossContingencyClaimsIncurredInPriorPeriods", attribute="debit", parent=opex2_15)

opex3_25 = Node("SellingExpense", attribute="debit", parent=opex2_21)
opex3_26 = Node("SalesCommissionsAndFees", attribute="debit", parent=opex2_21)
opex3_27 = Node("MarketingAndAdvertisingExpense", attribute="debit", parent=opex2_21)
opex3_28 = Node("FranchisorCosts", attribute="debit", parent=opex2_21)
opex3_29 = Node("ProductWarrantyExpense", attribute="debit", parent=opex2_21)
opex3_30 = Node("OtherSellingAndMarketingExpense", attribute="debit", parent=opex2_21)

opex3_31 = Node("AllocatedShareBasedCompensationExpense", attribute="debit", parent=opex2_22)
opex3_32 = Node("SalariesWagesAndOfficersCompensation", attribute="debit", parent=opex2_22)
opex3_33_1 = Node("LaborAndRelatedExpense", attribute="debit", parent=opex2_22)
opex3_33 = Node("OtherLaborRelatedExpenses", attribute="debit", parent=opex3_33_1)
opex3_34 = Node("ProfessionalFees", attribute="debit", parent=opex2_22)
opex3_35 = Node("BusinessDevelopment", attribute="debit", parent=opex2_22)
opex3_36 = Node("GeneralInsuranceExpense", attribute="debit", parent=opex2_22)
opex3_37 = Node("RealEstateInsurance", attribute="debit", parent=opex2_22)
opex3_38 = Node("CommunicationsInformationTechnologyAndOccupancy", attribute="debit", parent=opex2_22)
opex3_39 = Node("OperatingLeaseExpense", attribute="debit", parent=opex2_22)
opex3_40 = Node("TravelAndEntertainmentExpense", attribute="debit", parent=opex2_22)
opex3_41 = Node("SuppliesAndPostageExpense", attribute="debit", parent=opex2_22)
opex3_42 = Node("InsuranceTax", attribute="debit", parent=opex2_22)
opex3_43 = Node("TaxesExcludingIncomeAndExciseTaxes", attribute="debit", parent=opex2_22)
opex3_44 = Node("OtherGeneralAndAdministrativeExpense", attribute="debit", parent=opex2_22)
opex3_45 = Node("LossContingencyLossInPeriod", attribute="debit", parent=opex2_22)

# Level 4
opex4_1 = Node("AmortizationOfAcquisitionCosts", attribute="debit", parent=opex3_6)
opex4_2 = Node("AmortizationOfIntangibleAssets", attribute="debit", parent=opex3_6)
opex4_3 = Node("AmortizationOfDeferredSalesCommissions", attribute="debit", parent=opex3_6)
opex4_4 = Node("AmortizationOfRegulatoryAsset", attribute="debit", parent=opex3_6)
opex4_5 = Node("FinanceLeaseRightOfUseAssetAmortization", attribute="debit", parent=opex3_6)
opex4_6 = Node("AmortizationOfPowerContractsEmissionCredits", attribute="debit", parent=opex3_6)
opex4_7 = Node("AmortizationOfNuclearFuelLease", attribute="debit", parent=opex3_6)
opex4_8 = Node("AmortizationOfAdvanceRoyalty", attribute="debit", parent=opex3_6)
opex4_9 = Node("AmortizationOfDeferredPropertyTaxes", attribute="debit", parent=opex3_6)
opex4_10 = Node("AmortizationOfRateDeferral", attribute="debit", parent=opex3_6)
opex4_11 = Node("AmortizationOfDeferredHedgeGains", attribute="debit", parent=opex3_6)
opex4_12 = Node("AmortizationAndDepreciationOfDecontaminatingAndDecommissioningAssets", attribute="debit", parent=opex3_6)
opex4_13 = Node("OtherAmortizationOfDeferredCharges", attribute="debit", parent=opex3_6)

opex4_14 = Node("BusinessExitCosts1", attribute="debit", parent=opex3_8)
opex4_15 = Node("SeveranceCosts1", attribute="debit", parent=opex3_8)
opex4_16 = Node("OtherRestructuringCosts", attribute="debit", parent=opex3_8)

opex4_17 = Node("GoodwillAndIntangibleAssetImpairment", attribute="debit", parent=opex3_14)
opex4_18 = Node("EquityMethodInvestmentOtherThanTemporaryImpairment", attribute="debit", parent=opex3_14)
opex4_19 = Node("ImpairmentLossesRelatedToRealEstatePartnerships", attribute="debit", parent=opex3_14)
opex4_20 = Node("SalesTypeLeaseImpairmentLoss", attribute="debit", parent=opex3_14)
opex4_21 = Node("DirectFinancingLeaseImpairmentLoss", attribute="debit", parent=opex3_14)
opex4_22 = Node("ImpairmentOfLeasehold", attribute="debit", parent=opex3_14)
opex4_23 = Node("TangibleAssetImpairmentCharges", attribute="debit", parent=opex3_14)
opex4_24 = Node("AffordableHousingProjectInvestmentWriteDownAmount", attribute="debit", parent=opex3_14)

opex4_25 = Node("LegalFees", attribute="debit", parent=opex3_20)

opex4_26 = Node("EnvironmentalRemediationExpense", attribute="debit", parent=opex3_13)
opex4_27 = Node("EnvironmentalCostsRecognizedRecoveryCreditedToExpense", attribute="credit", parent=opex3_13)

opex4_28 = Node("MarketingExpense", attribute="debit", parent=opex3_27)
opex4_29 = Node("AdvertisingExpense", attribute="debit", parent=opex3_27)

opex4_30 = Node("CostsOfFranchisorOwnedOutlets", attribute="debit", parent=opex3_28)
opex4_31 = Node("CostsOfFranchisedOutlets", attribute="debit", parent=opex3_28)

opex4_32 = Node("CommunicationsAndInformationTechnology", attribute="debit", parent=opex3_38)
opex4_33 = Node("OccupancyNet", attribute="debit", parent=opex3_38)

opex4_34 = Node("SuppliesExpense", attribute="debit", parent=opex3_41)
opex4_35 = Node("PostageExpense", attribute="debit", parent=opex3_41)

opex4_36 = Node("RealEstateTaxExpense", attribute="debit", parent=opex3_43)
opex4_37 = Node("ProductionTaxExpense", attribute="debit", parent=opex3_43)
opex4_38 = Node("PumpTaxes", attribute="debit", parent=opex3_43)
opex4_39 = Node("TaxesOther", attribute="debit", parent=opex3_43)

"""
Nonoperating Income
"""
noi = Node("NonoperatingIncomeExpense", attribute="credit", parent=pti1_1)

# Level 1
noi1_1 = Node("InvestmentIncomeNonoperating", attribute="credit", parent=noi)
noi1_2 = Node("GainLossOnContractTermination", attribute="credit", parent=noi)
noi1_3 = Node("GainLossOnCondemnation", attribute="credit", parent=noi)
noi1_4 = Node("LossFromCatastrophes", attribute="debit", parent=noi)
noi1_5 = Node("PublicUtilitiesAllowanceForFundsUsedDuringConstructionAdditions", attribute="credit", parent=noi)
noi1_6 = Node("ForeignCurrencyTransactionGainLossBeforeTax", attribute="credit", parent=noi)
noi1_7 = Node("SalesTypeLeaseInitialDirectCostExpenseCommencement", attribute="debit", parent=noi)
noi1_8 = Node("OperatingLeaseInitialDirectCostExpenseOverTerm", attribute="debit", parent=noi)
noi1_9 = Node("GainLossOnSaleOfLeasedAssetsNetOperatingLeases", attribute="credit", parent=noi)
noi1_10 = Node("GainsLossesOnSalesOfOtherRealEstate", attribute="credit", parent=noi)
noi1_11 = Node("BankOwnedLifeInsuranceIncome", attribute="credit", parent=noi)
noi1_12 = Node("RealEstateInvestmentPartnershipRevenue", attribute="credit", parent=noi)
noi1_13 = Node("ConversionGainsAndLossesOnForeignInvestments", attribute="credit", parent=noi)
noi1_14 = Node("ProfitLossFromRealEstateOperations", attribute="credit", parent=noi)
noi1_15 = Node("MortgageServicingRightsMSRImpairmentRecovery", attribute="credit", parent=noi)
noi1_16 = Node("DebtInstrumentConvertibleBeneficialConversionFeature", attribute="credit", parent=noi)
noi1_17 = Node("PublicUtilitiesAllowanceForFundsUsedDuringConstructionCapitalizedCostOfEquity", attribute="credit", parent=noi)
noi1_18 = Node("NetPeriodicDefinedBenefitsExpenseReversalOfExpenseExcludingServiceCostComponent", attribute="debit", parent=noi)
noi1_19 = Node("OtherNonoperatingIncomeExpense", attribute="credit", parent=noi)
noi1_20 = Node("UnusualOrInfrequentItemNetGainLoss", attribute="debit", parent=noi)

# Level 2

noi2_1 = Node("NonoperatingGainsLosses", attribute="credit", parent=noi1_1)
noi2_2 = Node("RoyaltyIncomeNonoperating", attribute="credit", parent=noi1_1)
noi2_3 = Node("RentalIncomeNonoperating", attribute="credit", parent=noi1_1)
noi2_4 = Node("DevelopmentProfitsNonoperating", attribute="credit", parent=noi1_1)
noi2_5 = Node("RecoveryStrandedCosts", attribute="debit", parent=noi1_1)
noi2_6 = Node("LeveragedLeasesIncomeStatementNetIncomeFromLeveragedLeases", attribute="credit", parent=noi1_1)
noi2_7 = Node("InvestmentIncomeNet", attribute="credit", parent=noi1_1)

noi2_8 = Node("ForeignCurrencyTransactionGainLossRealized", attribute="credit", parent=noi1_6)
noi2_9 = Node("ForeignCurrencyTransactionGainLossUnrealized", attribute="credit", parent=noi1_6)

noi2_10 = Node("OtherNonoperatingIncome", attribute="credit", parent=noi1_19)
noi2_11 = Node("OtherNonoperatingExpense", attribute="debit", parent=noi1_19)

noi2_12 = Node("DiscontinuedApplicationOfSpecializedAccountingForRegulatedOperations", attribute="credit", parent=noi1_20)
noi2_13 = Node("UnusualOrInfrequentItemGainGross", attribute="credit", parent=noi1_20)
noi2_14 = Node("UnusualOrInfrequentItemNetOfInsuranceProceeds", attribute="debit", parent=noi1_20)

# Level 3

noi3_1 = Node("GainLossOnInvestments", attribute="credit", parent=noi2_1)
noi3_2 = Node("VentureCapitalGainsLossesNet", attribute="credit", parent=noi2_1)
noi3_3 = Node("DisposalGroupNotDiscontinuedOperationGainLossOnDisposal", attribute="credit", parent=noi2_1)
noi3_4 = Node("GainLossOnSaleOfStockInSubsidiaryOrEquityMethodInvestee", attribute="credit", parent=noi2_1)
noi3_5 = Node("DeconsolidationGainOrLossAmount", attribute="credit", parent=noi2_1)
noi3_6 = Node("GainLossOnSaleOfPreviouslyUnissuedStockBySubsidiaryOrEquityInvesteeNonoperatingIncome", attribute="credit", parent=noi2_1)
noi3_7 = Node("GainLossOnSaleOfInterestInProjects", attribute="credit", parent=noi2_1)
noi3_8 = Node("GainLossOnDerivativeInstrumentsNetPretax", attribute="credit", parent=noi2_1)
noi3_9 = Node("BusinessCombinationBargainPurchaseGainRecognizedAmount", attribute="credit", parent=noi2_1)
noi3_10 = Node("OtherNonoperatingGainsLosses", attribute="credit", parent=noi2_1)

noi3_11 = Node("LeveragedLeasesIncomeStatementIncomeFromLeveragedLeases", attribute="credit", parent=noi2_6)
noi3_12 = Node("LeveragedLeasesIncomeStatementIncomeTaxExpenseOnLeveragedLeases", attribute="debit", parent=noi2_6)
noi3_13 = Node("LeveragedLeasesIncomeStatementInvestmentTaxCreditRecognizedOnLeveragedLeases", attribute="credit", parent=noi2_6)

noi3_14 = Node("InvestmentIncomeInterestAndDividend", attribute="credit", parent=noi2_6)
noi3_15 = Node("InvestmentIncomeNetAmortizationOfDiscountAndPremium", attribute="credit", parent=noi2_6)
noi3_16 = Node("InvestmentIncomeInvestmentExpense", attribute="debit", parent=noi2_6)

noi3_17 = Node("OtherNonoperatingAssetRelatedIncome", attribute="credit", parent=noi2_10)

noi3_18 = Node("UnusualOrInfrequentItemInsuranceProceeds", attribute="credit", parent=noi2_14)
noi3_19 = Node("UnusualOrInfrequentItemLossGross", attribute="debit", parent=noi2_14)

# Level 4

noi4_1 = Node("EquityMethodInvestmentRealizedGainLossOnDisposal", attribute="credit", parent=noi3_4)
noi4_2 = Node("GainOrLossOnSaleOfStockInSubsidiary", attribute="credit", parent=noi3_4)

noi4_3 = Node("GainOrLossOnSaleOfPreviouslyUnissuedStockBySubsidiary", attribute="credit", parent=noi3_6)
noi4_4 = Node("GainOrLossOnSaleOfPreviouslyUnissuedStockByEquityInvestee", attribute="credit", parent=noi3_6)

noi4_5 = Node("GainLossFromPriceRiskManagementActivity", attribute="credit", parent=noi3_8)
noi4_6 = Node("GainLossOnOilAndGasHedgingActivity", attribute="credit", parent=noi3_8)
noi4_7 = Node("DerivativeInstrumentsNotDesignatedAsHedgingInstrumentsGainLossNet", attribute="credit", parent=noi3_8)

noi4_8 = Node("InvestmentIncomeInterest", attribute="credit", parent=noi3_14)
noi4_9 = Node("InvestmentIncomeDividend", attribute="credit", parent=noi3_14)

noi4_10 = Node("InvestmentIncomeAmortizationOfDiscount", attribute="credit", parent=noi3_15)
noi4_11 = Node("InvestmentIncomeAmortizationOfPremium", attribute="credit", parent=noi3_15)

# Level 5

noi5_1 = Node("GainLossOnInterestRateDerivativeInstrumentsNotDesignatedAsHedgingInstruments", attribute="credit", parent=noi4_7)
noi5_2 = Node("GainLossOnDerivativeInstrumentsHeldForTradingPurposesNet", attribute="credit", parent=noi4_7)

noi5_3 = Node("InterestIncomeRelatedParty", attribute="credit", parent=noi4_8)

"""
Costs and Expenses
"""

ce = Node("CostsAndExpenses", attribute="credit")

"""
Net Interest Income/Expense
"""

nii = Node("InterestRevenueExpenseNet", attribute="credit")
nii1_1 = Node("InterestIncomeExpenseNet", attribute="credit", parent=nii)

"""
Interest and Debt Expense
"""

ide = Node("InterestAndDebtExpense", attribute="debit", parent=pti1_1)

# Level 1

ide1_1 = Node("InterestExpense", attribute="debit", parent=ide)
ide1_2 = Node("GainsLossesOnExtinguishmentOfDebt", attribute="credit", parent=ide)
ide1_3 = Node("InducedConversionOfConvertibleDebtExpense", attribute="debit", parent=ide)
ide1_4 = Node("GainsLossesOnRestructuringOfDebt", attribute="credit", parent=ide)
ide1_5 = Node("GainsLossesOnRecourseDebt", attribute="credit", parent=ide)
ide1_6 = Node("GainLossOnNonRecourseDebt", attribute="credit", parent=ide)
ide1_7 = Node("GainLossOnRepurchaseOfDebtInstrument", attribute="debit", parent=ide)
ide1_8 = Node("DistributionsOnMandatorilyRedeemableSecurities", attribute="credit", parent=ide)

# Level 2

ide2_1 = Node("InterestExpenseDebt", attribute="debit", parent=ide1_1)
ide2_2 = Node("InterestExpenseCustomerDeposits", attribute="debit", parent=ide1_1)
ide2_3 = Node("DebtRelatedCommitmentFeesAndDebtIssuanceCosts", attribute="debit", parent=ide1_1)
ide2_4 = Node("FinanceLeaseInterestExpense", attribute="debit", parent=ide1_1)
ide2_5 = Node("InterestExpenseRelatedParty", attribute="debit", parent=ide1_1)
ide2_6 = Node("InterestExpenseOther", attribute="debit", parent=ide1_1)
ide2_7 = Node("InterestExpenseDeposits", attribute="debit", parent=ide1_1)
ide2_8 = Node("InterestExpenseTradingLiabilities", attribute="debit", parent=ide1_1)
ide2_9 = Node("InterestExpenseBorrowings", attribute="debit", parent=ide1_1)
ide2_10 = Node("InterestExpenseBeneficialInterestsIssuedByConsolidatedVariableInterestEntities", attribute="debit", parent=ide1_1)
ide2_11 = Node("InterestExpenseTrustPreferredSecurities", attribute="debit", parent=ide1_1)

ide2_10 = Node("GainsLossesOnExtinguishmentOfDebtBeforeWriteOffOfDeferredDebtIssuanceCost", attribute="credit",
               parent=ide1_2)
ide2_11 = Node("WriteOffOfDeferredDebtIssuanceCost", attribute="debit", parent=ide1_2)

# Level 3
ide3_1 = Node("InterestExpenseDomesticDeposits", attribute="debit", parent=ide2_7)
ide3_2 = Node("InterestExpenseForeignDeposits", attribute="debit", parent=ide2_7)

ide3_3 = Node("InterestExpenseShortTermBorrowings", attribute="debit", parent=ide2_9)
ide3_4 = Node("InterestExpenseLongTermDebtAndCapitalSecurities", attribute="debit", parent=ide2_9)

# Level 4
ide4_1 = Node("InterestExpenseNOWAccountsMoneyMarketAccountsAndSavingsDeposits", attribute="debit", parent=ide3_1)
ide4_2 = Node("InterestExpenseDemandDepositAccounts", attribute="debit", parent=ide3_1)
ide4_3 = Node("InterestExpenseTimeDeposits", attribute="debit", parent=ide3_1)
ide4_4 = Node("InterestExpenseOtherDomesticDeposits", attribute="debit", parent=ide3_1)

ide4_5 = Node("InterestExpenseFederalFundsPurchasedAndSecuritiesSoldUnderAgreementsToRepurchase", attribute="debit", parent=ide3_3)
ide4_6 = Node("InterestExpenseShortTermBorrowingsExcludingFederalFundsAndSecuritiesSoldUnderAgreementsToRepurchase", attribute="debit", parent=ide3_3)

ide4_7 = Node("InterestExpenseLongTermDebt", attribute="debit", parent=ide3_4)
ide4_8 = Node("InterestExpenseCapitalSecurities", attribute="debit", parent=ide3_4)

# Level 5

ide5_1 = Node("InterestExpenseNegotiableOrderOfWithdrawalNOWDeposits", attribute="debit", parent=ide4_1)
ide5_2 = Node("InterestExpenseMoneyMarketDeposits", attribute="debit", parent=ide4_1)
ide5_3 = Node("InterestExpenseSavingsDeposits", attribute="debit", parent=ide4_1)

ide5_4 = Node("InterestExpenseTimeDepositsLessThan100000", attribute="debit", parent=ide4_3)
ide5_5 = Node("InterestExpenseTimeDeposits100000OrMore", attribute="debit", parent=ide4_3)

ide5_6 = Node("InterestExpenseFederalFundsPurchased", attribute="debit", parent=ide4_5)
ide5_7 = Node("InterestExpenseSecuritiesSoldUnderAgreementsToRepurchase", attribute="debit", parent=ide4_5)

ide5_8 = Node("InterestExpenseFederalHomeLoanBankAndFederalReserveBankAdvancesShortTerm", attribute="debit", parent=ide4_6)
ide5_9 = Node("InterestExpenseCommercialPaper", attribute="debit", parent=ide4_6)
ide5_10 = Node("InterestExpenseOtherShortTermBorrowings", attribute="debit", parent=ide4_6)

ide5_11 = Node("InterestExpenseSubordinatedNotesAndDebentures", attribute="debit", parent=ide4_7)
ide5_12 = Node("InterestExpenseJuniorSubordinatedDebentures", attribute="debit", parent=ide4_7)
ide5_13 = Node("InterestExpenseMediumTermNotes", attribute="debit", parent=ide4_7)
ide5_14 = Node("InterestExpenseFederalHomeLoanBankAndFederalReserveBankAdvancesLongTerm", attribute="debit",
               parent=ide4_7)
ide5_15 = Node("InterestExpenseOtherLongTermDebt", attribute="debit", parent=ide4_7)

"""
Assets
"""

a = Node("Assets", attribute="debit")

"""
Liabilities
"""
l = Node("Liabilities", attribute="credit")

"""
Current Assets
"""
ca1 = Node("CurrentAssets", attribute="debit", parent=a)
ca = Node("AssetsCurrent", attribute="debit", parent=ca1)

# Level 1
ca1_1 = Node("CashCashEquivalentsAndShortTermInvestments", attribute="debit", parent=ca)
ca1_1_1 = Node("CashAndCashEquivalents", attribute="debit", parent=ca1_1)
ca1_2 = Node("NetInvestmentInLeaseCurrent", attribute="debit", parent=ca)
ca1_3 = Node("RestrictedCashAndInvestmentsCurrent", attribute="debit", parent=ca)

ca1_4 = Node("ReceivablesNetCurrent", attribute="debit", parent=ca)
ca1_35 = Node("AccountsAndOtherReceivablesNetCurrent", attribute="debit", parent=ca1_4)
ca1_35_1 = Node("CurrentReceivablesFromContractsWithCustomers", attribute="debit", parent=ca1_35) #IFRS
ca1_35_2 = Node("TradeAndOtherCurrentReceivables", attribute="debit", parent=ca1_35_1) #IFRS

ca1_5 = Node("InventoryNetOfAllowancesCustomerAdvancesAndProgressBillings", attribute="debit", parent=ca)
ca1_6 = Node("PrepaidExpenseCurrent", attribute="debit", parent=ca)
ca1_7 = Node("ContractWithCustomerAssetNetCurrent", attribute="debit", parent=ca)
ca1_8 = Node("CapitalizedContractCostNetCurrent", attribute="debit", parent=ca)
ca1_9 = Node("DeferredCostsCurrent", attribute="debit", parent=ca)
ca1_10 = Node("DerivativeInstrumentsAndHedges", attribute="debit", parent=ca)
ca1_11 = Node("RegulatoryAssetsCurrent", attribute="debit", parent=ca)
ca1_12 = Node("FundsHeldForClients", attribute="debit", parent=ca)
ca1_13 = Node("DeferredRentAssetNetCurrent", attribute="debit", parent=ca)
ca1_14 = Node("AssetsHeldInTrustCurrent", attribute="debit", parent=ca)
ca1_15 = Node("AdvancesOnInventoryPurchases", attribute="debit", parent=ca)
ca1_16 = Node("FinancingReceivableAccruedInterestAfterAllowanceForCreditLoss", attribute="debit", parent=ca)
ca1_17 = Node("AccountsReceivableNoncurrentAccruedInterestAfterAllowanceForCreditLoss", attribute="debit", parent=ca)
ca1_18 = Node("DebtSecuritiesHeldToMaturityAccruedInterestAfterAllowanceForCreditLoss", attribute="debit", parent=ca)
ca1_19 = Node("NetInvestmentInLeaseAccruedInterestAfterAllowanceForCreditLoss", attribute="debit", parent=ca)
ca1_20 = Node("SalesTypeLeaseNetInvestmentInLeaseAccruedInterestAfterAllowanceForCreditLoss", attribute="debit", parent=ca)
ca1_21 = Node("DirectFinancingLeaseNetInvestmentInLeaseAccruedInterestAfterAllowanceForCreditLoss", attribute="debit", parent=ca)
ca1_22 = Node("FinancialAssetAmortizedCostAccruedInterestAfterAllowanceForCreditLoss", attribute="debit", parent=ca)
ca1_23 = Node("DebtSecuritiesAvailableForSaleAccruedInterestAfterAllowanceForCreditLossCurrent", attribute="debit", parent=ca)
ca1_24 = Node("FinancingReceivableExcludingAccruedInterestAfterAllowanceForCreditLossCurrent", attribute="debit", parent=ca)
ca1_25 = Node("DebtSecuritiesHeldToMaturityExcludingAccruedInterestAfterAllowanceForCreditLossCurrent", attribute="debit", parent=ca)
ca1_26 = Node("NetInvestmentInLeaseExcludingAccruedInterestAfterAllowanceForCreditLossCurrent", attribute="debit", parent=ca)
ca1_27 = Node("DebtSecuritiesAvailableForSaleAmortizedCostExcludingAccruedInterestAfterAllowanceForCreditLossCurrent", attribute="debit", parent=ca)
ca1_28 = Node("AdvanceRoyaltiesCurrent", attribute="debit", parent=ca)
ca1_29 = Node("AssetsOfDisposalGroupIncludingDiscontinuedOperationCurrent", attribute="debit", parent=ca)
ca1_30 = Node("AssetsHeldForSaleNotPartOfDisposalGroupCurrent", attribute="debit", parent=ca)
ca1_31 = Node("DepositsAssetsCurrent", attribute="debit", parent=ca)
ca1_32 = Node("IntangibleAssetsCurrent", attribute="debit", parent=ca)
ca1_33 = Node("BusinessCombinationContingentConsiderationAssetCurrent", attribute="debit", parent=ca)
ca1_34 = Node("OtherAssetsCurrent", attribute="debit", parent=ca)

# Level 2
ca2_1 = Node("CashAndCashEquivalentsAtCarryingValue", attribute="debit", parent=ca1_1_1)
ca2_1_1 = Node("Cash", attribute="debit", parent=ca2_1) # IFRS
ca2_2 = Node("ShortTermInvestments", attribute="debit", parent=ca1_1_1)
ca2_2_1 = Node("CashEquivalents", attribute="debit", parent=ca2_2) #IFRS

ca2_3 = Node("RestrictedCashAndCashEquivalentsAtCarryingValue", attribute="debit", parent=ca1_3)
ca2_4 = Node("RestrictedInvestmentsCurrent", attribute="debit", parent=ca1_3)
ca2_5 = Node("OtherRestrictedAssetsCurrent", attribute="debit", parent=ca1_3)

ca2_6 = Node("AccountsNotesAndLoansReceivableNetCurrent", attribute="debit", parent=ca1_35_2)
ca2_7 = Node("NontradeReceivablesCurrent", attribute="debit", parent=ca1_35_2)
ca2_8 = Node("UnbilledReceivablesCurrent", attribute="debit", parent=ca1_35_2)
ca2_9 = Node("ReceivablesLongTermContractsOrPrograms", attribute="debit", parent=ca1_35_2)
ca2_10 = Node("AccountsReceivableFromSecuritization", attribute="debit", parent=ca1_35_2)
ca2_11 = Node("OtherReceivablesNetCurrent", attribute="debit", parent=ca1_35_2)
ca2_42 = Node("CurrentTradeReceivables", attribute="debit", parent=ca1_35_2) #IFRS
ca2_43 = Node("CurrentPrepayments", attribute="debit", parent=ca1_35_2) #IFRS
ca2_44 = Node("OtherCurrentReceivables", attribute="debit", parent=ca1_35_2) #IFRS

ca2_12 = Node("InventoryNet", attribute="debit", parent=ca1_5)
ca2_12_1 = Node("Inventories", attribute="debit", parent=ca2_12) #IFRS
ca2_13 = Node("ProgressPaymentsNettedAgainstInventoryForLongTermContractsOrPrograms", attribute="debit", parent=ca1_5)

ca2_14 = Node("FinancingReceivableExcludingAccruedInterestBeforeAllowanceForCreditLossCurrent", attribute="debit",
              parent=ca1_24)
ca2_15 = Node("FinancingReceivableAllowanceForCreditLossExcludingAccruedInterestCurrent", attribute="credit",
              parent=ca1_24)

ca2_16 = Node("DebtSecuritiesHeldToMaturityExcludingAccruedInterestBeforeAllowanceForCreditLossCurrent",
              attribute="debit", parent=ca1_25)
ca2_17 = Node("DebtSecuritiesHeldToMaturityAllowanceForCreditLossExcludingAccruedInterestCurrent", attribute="credit",
              parent=ca1_25)

ca2_18 = Node("NetInvestmentInLeaseExcludingAccruedInterestBeforeAllowanceForCreditLossCurrent", attribute="debit",
              parent=ca1_26)
ca2_19 = Node("NetInvestmentInLeaseAllowanceForCreditLossExcludingAccruedInterestCurrent", attribute="credit",
              parent=ca1_26)

ca2_20 = Node("DebtSecuritiesAvailableForSaleAmortizedCostExcludingAccruedInterestBeforeAllowanceForCreditLossCurrent", attribute="debit", parent=ca1_27)
ca2_21 = Node("DebtSecuritiesAvailableForSaleAmortizedCostAllowanceForCreditLossExcludingAccruedInterestCurrent", attribute="credit", parent=ca1_27)

ca2_22 = Node("DisposalGroupIncludingDiscontinuedOperationCashAndCashEquivalents", attribute="debit", parent=ca1_29)
ca2_23 = Node("DisposalGroupIncludingDiscontinuedOperationInventoryCurrent", attribute="debit", parent=ca1_29)
ca2_24 = Node("DisposalGroupIncludingDiscontinuedOperationOtherCurrentAssets", attribute="debit", parent=ca1_29)
ca2_25 = Node("DisposalGroupIncludingDiscontinuedOperationAccountsNotesAndLoansReceivableNet", attribute="debit",
              parent=ca1_29)
ca2_26 = Node("DisposalGroupIncludingDiscontinuedOperationGoodwillCurrent", attribute="debit", parent=ca1_29)
ca2_27 = Node("DisposalGroupIncludingDiscontinuedOperationPropertyPlantAndEquipmentCurrent", attribute="debit",
              parent=ca1_29)
ca2_28 = Node("DisposalGroupIncludingDiscontinuedOperationIntangibleAssetsCurrent", attribute="debit", parent=ca1_29)

ca2_29 = Node("TradeAndLoansReceivablesHeldForSaleNetNotPartOfDisposalGroup", attribute="debit", parent=ca1_30)
ca2_30 = Node("AssetsHeldForSaleNotPartOfDisposalGroupCurrentOther", attribute="debit", parent=ca1_30)

ca2_31 = Node("DerivativeAssetsCurrent", attribute="debit", parent=ca1_10)
ca2_32 = Node("HedgingAssetsCurrent", attribute="debit", parent=ca1_10)
ca2_33 = Node("CommodityContractAssetCurrent", attribute="debit", parent=ca1_10)
ca2_34 = Node("EnergyMarketingContractsAssetsCurrent", attribute="debit", parent=ca1_10)

ca2_29 = Node("DeferredCostsLeasingNetCurrent", attribute="debit", parent=ca1_9)
ca2_30 = Node("DeferredFuelCost", attribute="debit", parent=ca1_9)
ca2_31 = Node("DeferredStormAndPropertyReserveDeficiencyCurrent", attribute="debit", parent=ca1_9)
ca2_32 = Node("OtherDeferredCostsNet", attribute="debit", parent=ca1_9)
ca2_33 = Node("DeferredOfferingCosts", attribute="debit", parent=ca1_9)

ca2_34 = Node("PrepaidInsurance", attribute="debit", parent=ca1_6)
ca2_35 = Node("PrepaidRent", attribute="debit", parent=ca1_6)
ca2_36 = Node("PrepaidAdvertising", attribute="debit", parent=ca1_6)
ca2_37 = Node("PrepaidRoyalties", attribute="debit", parent=ca1_6)
ca2_38 = Node("Supplies", attribute="debit", parent=ca1_6)
ca2_39 = Node("PrepaidInterest", attribute="debit", parent=ca1_6)
ca2_40 = Node("PrepaidTaxes", attribute="debit", parent=ca1_6)
ca2_41 = Node("OtherPrepaidExpenseCurrent", attribute="debit", parent=ca1_6)

# Level 3
ca3_1 = Node("CashAndDueFromBanks", attribute="debit", parent=ca2_1_1)
ca3_1_1 = Node("BalancesWithBanks", attribute="debit", parent=ca3_1) #IFRS
ca3_2 = Node("InterestBearingDepositsInBanks", attribute="debit", parent=ca2_1_1)
ca3_3 = Node("CashEquivalentsAtCarryingValue", attribute="debit", parent=ca2_1_1)

ca3_4 = Node("EquitySecuritiesFvNi", attribute="debit", parent=ca2_2_1)
ca3_5 = Node("DebtSecuritiesCurrent", attribute="debit", parent=ca2_2_1)
ca3_6 = Node("MarketableSecuritiesCurrent", attribute="debit", parent=ca2_2_1)
ca3_7 = Node("OtherShortTermInvestments", attribute="debit", parent=ca2_2_1)

ca3_8 = Node("RestrictedCashCurrent", attribute="debit", parent=ca2_3)
ca3_9 = Node("RestrictedCashEquivalentsCurrent", attribute="debit", parent=ca2_3)

ca3_10 = Node("InventoryGross", attribute="debit", parent=ca2_12_1)
ca3_11 = Node("InventoryAdjustments", attribute="credit", parent=ca2_12_1)

ca3_12 = Node("AccountsReceivableNetCurrent", attribute="debit", parent=ca2_6)
ca3_13 = Node("NotesAndLoansReceivableNetCurrent", attribute="credit", parent=ca2_6)

ca3_14 = Node("AllowanceForDoubtfulOtherReceivablesCurrent", attribute="debit", parent=ca2_11)
ca3_15 = Node("OtherReceivablesGrossCurrent", attribute="credit", parent=ca2_11)

ca3_16 = Node("DeferredGasCost", attribute="debit", parent=ca2_30)

ca3_17 = Node("OtherDeferredCostsGross", attribute="debit", parent=ca2_32)
ca3_18 = Node("AccumulatedAmortizationOfOtherDeferredCosts", attribute="credit", parent=ca2_32)

# Level 4
ca4_1 = Node("Cash", attribute="debit", parent=ca3_1_1)
ca4_2 = Node("DueFromBanks", attribute="debit", parent=ca3_1_1)

ca4_3 = Node("TradingSecuritiesDebt", attribute="debit", parent=ca3_5)
ca4_4 = Node("AvailableForSaleSecuritiesDebtSecuritiesCurrent", attribute="debit", parent=ca3_5)
ca4_5 = Node("DebtSecuritiesHeldToMaturityAmortizedCostAfterAllowanceForCreditLossCurrent", attribute="debit",
             parent=ca3_5)

ca4_6 = Node("AccountsReceivableGrossCurrent", attribute="debit", parent=ca3_12)
ca4_7 = Node("AllowanceForDoubtfulAccountsReceivableCurrent", attribute="credit", parent=ca3_12)

ca4_8 = Node("AirlineRelatedInventory", attribute="debit", parent=ca3_10)
ca4_9 = Node("RetailRelatedInventory", attribute="debit", parent=ca3_10)
ca4_10 = Node("EnergyRelatedInventory", attribute="debit", parent=ca3_10)
ca4_11 = Node("AgriculturalRelatedInventory", attribute="debit", parent=ca3_10)
ca4_12 = Node("PublicUtilitiesInventory", attribute="debit", parent=ca3_10)

ca4_13 = Node("InventoryValuationReserves", attribute="credit", parent=ca3_11)
ca4_14 = Node("InventoryLIFOReserve", attribute="credit", parent=ca3_11)

ca4_15 = Node("AssetBackedSecuritiesAtCarryingValue", attribute="debit", parent=ca3_3)
ca4_16 = Node("CertificatesOfDepositAtCarryingValue", attribute="debit", parent=ca3_3)
ca4_17 = Node("CommercialPaperAtCarryingValue", attribute="debit", parent=ca3_3)
ca4_18 = Node("CreditAndDebitCardReceivablesAtCarryingValue", attribute="debit", parent=ca3_3)
ca4_19 = Node("MoneyMarketFundsAtCarryingValue", attribute="debit", parent=ca3_3)
ca4_20 = Node("MunicipalDebtSecuritiesAtCarryingValue", attribute="debit", parent=ca3_3)
ca4_21 = Node("TimeDepositsAtCarryingValue", attribute="debit", parent=ca3_3)
ca4_22 = Node("USGovernmentSecuritiesAtCarryingValue", attribute="debit", parent=ca3_3)
ca4_23 = Node("USGovernmentAgenciesSecuritiesAtCarryingValue", attribute="debit", parent=ca3_3)
ca4_24 = Node("OtherCashEquivalentsAtCarryingValue", attribute="debit", parent=ca3_3)

# Level 5
ca5_1 = Node("HeldToMaturitySecuritiesCurrent", attribute="debit", parent=ca4_5)
ca5_2 = Node("DebtSecuritiesHeldToMaturityAllowanceForCreditLossCurrent", attribute="credit", parent=ca4_5)

ca4_8 = Node("AirlineRelatedInventoryAircraftFuel", attribute="debit", parent=ca4_8)
ca4_9 = Node("AirlineRelatedInventoryAircraftParts", attribute="debit", parent=ca4_8)

ca4_10 = Node("RetailRelatedInventoryMerchandise", attribute="debit", parent=ca4_9)
ca4_11 = Node("RetailRelatedInventoryPackagingAndOtherSupplies", attribute="debit", parent=ca4_9)

ca4_12 = Node("EnergyRelatedInventoryPetroleum", attribute="debit", parent=ca4_10)
ca4_13 = Node("EnergyRelatedInventoryNaturalGasLiquids", attribute="debit", parent=ca4_10)
ca4_14 = Node("EnergyRelatedInventoryNaturalGasInStorage", attribute="debit", parent=ca4_10)
ca4_15 = Node("EnergyRelatedInventoryGasStoredUnderground", attribute="debit", parent=ca4_10)
ca4_16 = Node("EnergyRelatedInventoryPropaneGas", attribute="debit", parent=ca4_10)
ca4_17 = Node("EnergyRelatedInventoryCoal", attribute="debit", parent=ca4_10)
ca4_18 = Node("EnergyRelatedInventoryChemicals", attribute="debit", parent=ca4_10)
ca4_19 = Node("EnergyRelatedInventoryOtherFossilFuel", attribute="debit", parent=ca4_10)
ca4_20 = Node("CrudeOilAndNaturalGasLiquids", attribute="debit", parent=ca4_10)
ca4_21 = Node("InventoryCrudeOilProductsAndMerchandise", attribute="debit", parent=ca4_10)

ca4_22 = Node("AgriculturalRelatedInventoryPlantMaterial", attribute="debit", parent=ca4_11)
ca4_23 = Node("AgriculturalRelatedInventoryGrowingCrops", attribute="debit", parent=ca4_11)
ca4_24 = Node("AgriculturalRelatedInventoryFeedAndSupplies", attribute="debit", parent=ca4_11)

ca4_25 = Node("ConstructionContractorReceivableIncludingContractRetainageYearOne", attribute="debit", parent=ca4_6)
ca4_26 = Node("ConstructionContractorReceivableRetainageYearOne", attribute="debit", parent=ca4_6)
ca4_27 = Node("ContractReceivableDueOneYearOrLess", attribute="debit", parent=ca4_6)

"""
Non-current Assets
"""
nca = Node("AssetsNoncurrent", attribute="debit", parent=a)

# Level 1

nca1_1 = Node("InventoryNoncurrent", attribute="debit", parent=nca)
nca1_2 = Node("FinanceLeaseRightOfUseAsset", attribute="debit", parent=nca)
nca1_3 = Node("OperatingLeaseRightOfUseAsset", attribute="debit", parent=nca)
nca1_4 = Node("NetInvestmentInLeaseNoncurrent", attribute="debit", parent=nca)
nca1_5 = Node("AccountsReceivableExcludingAccruedInterestAfterAllowanceForCreditLossNoncurrent", attribute="debit",
              parent=nca)
nca1_6 = Node("FinancingReceivableExcludingAccruedInterestAfterAllowanceForCreditLossNoncurrent", attribute="debit",
              parent=nca)
nca1_7 = Node("DebtSecuritiesHeldToMaturityExcludingAccruedInterestAfterAllowanceForCreditLossNoncurrent", attribute="debit", parent=nca)
nca1_8 = Node("NetInvestmentInLeaseExcludingAccruedInterestAfterAllowanceForCreditLossNoncurrent", attribute="debit", parent=nca)
nca1_9 = Node("DebtSecuritiesAvailableForSaleAmortizedCostExcludingAccruedInterestAfterAllowanceForCreditLossNoncurrent", attribute="debit", parent=nca)
nca1_10 = Node("LeveragedLeasesNetInvestmentInLeveragedLeasesDisclosureInvestmentInLeveragedLeasesNet", attribute="debit", parent=nca)
nca1_11 = Node("InventoryRealEstate", attribute="debit", parent=nca)
nca1_12 = Node("NontradeReceivablesNoncurrent", attribute="debit", parent=nca)
nca1_13 = Node("PropertyPlantAndEquipmentNet", attribute="debit", parent=nca)
nca1_13_1 = Node("PropertyPlantAndEquipmentIncludingRightofuseAssets", attribute="debit", parent=nca1_13)
nca1_14 = Node("PropertyPlantAndEquipmentCollectionsNotCapitalized", attribute="debit", parent=nca)
nca1_15 = Node("DebtSecuritiesAvailableForSaleAccruedInterestAfterAllowanceForCreditLossNoncurrent", attribute="debit", parent=nca)
nca1_16 = Node("OilAndGasPropertySuccessfulEffortMethodNet", attribute="debit", parent=nca)
nca1_17 = Node("OilAndGasPropertyFullCostMethodNet", attribute="debit", parent=nca)
nca1_18 = Node("LongTermInvestmentsAndReceivablesNet", attribute="debit", parent=nca)
nca1_19 = Node("IntangibleAssetsNetIncludingGoodwill", attribute="debit", parent=nca)
nca1_19_1 = Node("IntangibleAssetsAndGoodwill", attribute="debit", parent=nca1_19)
nca1_20 = Node("PrepaidExpenseNoncurrent", attribute="debit", parent=nca)
nca1_21 = Node("ContractWithCustomerAssetNetNoncurrent", attribute="debit", parent=nca)
nca1_22 = Node("CapitalizedContractCostNetNoncurrent", attribute="debit", parent=nca)
nca1_23 = Node("DerivativeInstrumentsAndHedgesNoncurrent", attribute="debit", parent=nca)
nca1_24 = Node("RegulatedEntityOtherAssetsNoncurrent", attribute="debit", parent=nca)
nca1_25 = Node("DepositsAssetsNoncurrent", attribute="debit", parent=nca)
nca1_26 = Node("DeferredRentReceivablesNetNoncurrent", attribute="debit", parent=nca)
nca1_27 = Node("AssetsHeldInTrustNoncurrent", attribute="debit", parent=nca)
nca1_28 = Node("RestrictedCashAndInvestmentsNoncurrent", attribute="debit", parent=nca)
nca1_29 = Node("DisposalGroupIncludingDiscontinuedOperationAssetsNoncurrent", attribute="debit", parent=nca)
nca1_30 = Node("AdvanceRoyaltiesNoncurrent", attribute="debit", parent=nca)
nca1_31 = Node("EstimatedInsuranceRecoveries", attribute="debit", parent=nca)
nca1_32 = Node("CustomerFunds", attribute="debit", parent=nca)
nca1_33 = Node("DeferredCosts", attribute="debit", parent=nca)
nca1_34 = Node("DeferredIncomeTaxAssetsNet", attribute="debit", parent=nca)
nca1_35 = Node("BusinessCombinationContingentConsiderationAssetNoncurrent", attribute="debit", parent=nca)
nca1_36 = Node("OtherAssetsNoncurrent", attribute="debit", parent=nca)
nca1_37 = Node("AmortizationMethodQualifiedAffordableHousingProjectInvestments", attribute="debit", parent=nca)
nca1_38 = Node("OtherReceivableAfterAllowanceForCreditLossNoncurrent", attribute="debit", parent=nca)

# Level 2

nca2_1 = Node("InventoryDrillingNoncurrent", attribute="debit", parent=nca1_1)
nca2_2 = Node("InventoryGasInStorageUndergroundNoncurrent", attribute="debit", parent=nca1_1)
nca2_3 = Node("OtherInventoryNoncurrent", attribute="debit", parent=nca1_1)

nca2_4 = Node("AccountsReceivableExcludingAccruedInterestBeforeAllowanceForCreditLossNoncurrent", attribute="debit", parent=nca1_5)
nca2_5 = Node("AccountsReceivableAllowanceForCreditLossExcludingAccruedInterestNoncurrent", attribute="credit", parent=nca1_5)

nca2_6 = Node("FinancingReceivableExcludingAccruedInterestBeforeAllowanceForCreditLossNoncurrent", attribute="debit", parent=nca1_6)
nca2_7 = Node("FinancingReceivableAllowanceForCreditLossExcludingAccruedInterestNoncurrent", attribute="credit", parent=nca1_6)

nca2_8 = Node("DebtSecuritiesHeldToMaturityExcludingAccruedInterestBeforeAllowanceForCreditLossNoncurrent", attribute="debit", parent=nca1_7)
nca2_9 = Node("DebtSecuritiesHeldToMaturityAllowanceForCreditLossExcludingAccruedInterestNoncurrent", attribute="credit", parent=nca1_7)

nca2_10 = Node("NetInvestmentInLeaseExcludingAccruedInterestBeforeAllowanceForCreditLossNoncurrent", attribute="debit", parent=nca1_8)
nca2_11 = Node("NetInvestmentInLeaseAllowanceForCreditLossExcludingAccruedInterestNoncurrent", attribute="credit", parent=nca1_8)

nca2_12 = Node("DebtSecuritiesAvailableForSaleAmortizedCostExcludingAccruedInterestBeforeAllowanceForCreditLossNoncurrent", attribute="debit", parent=nca1_9)
nca2_13 = Node("DebtSecuritiesAvailableForSaleAmortizedCostAllowanceForCreditLossExcludingAccruedInterestNoncurrent", attribute="credit", parent=nca1_9)

nca2_13 = Node("InventoryRealEstateImprovements", attribute="debit", parent=nca1_11)
nca2_14 = Node("InventoryRealEstateHeldForSale", attribute="debit", parent=nca1_11)
nca2_15 = Node("InventoryRealEstateLandAndLandDevelopmentCosts", attribute="debit", parent=nca1_11)
nca2_16 = Node("InventoryRealEstateConstructionInProcess", attribute="debit", parent=nca1_11)
nca2_17 = Node("InventoryRealEstateMortgageLoansHeldInInventory", attribute="debit", parent=nca1_11)
nca2_18 = Node("InventoryOperativeBuilders", attribute="debit", parent=nca1_11)
nca2_19 = Node("InventoryRealEstateTimeshareAvailableForSale", attribute="debit", parent=nca1_11)
nca2_20 = Node("InventoryRealEstateOther", attribute="debit", parent=nca1_11)

nca2_21 = Node("InterestReceivableNoncurrent", attribute="debit", parent=nca1_12)
nca2_22 = Node("IncomeTaxesReceivableNoncurrent", attribute="debit", parent=nca1_12)
nca2_23 = Node("ValueAddedTaxReceivableNoncurrent", attribute="debit", parent=nca1_12)
nca2_24 = Node("InsuranceSettlementsReceivableNoncurrent", attribute="debit", parent=nca1_12)
nca2_25 = Node("GrantsReceivableNoncurrent", attribute="debit", parent=nca1_12)
nca2_26 = Node("InsuranceReceivableForMalpracticeNoncurrent", attribute="debit", parent=nca1_12)
nca2_27 = Node("OilAndGasJointInterestBillingReceivablesNoncurrent", attribute="debit", parent=nca1_12)

nca2_28 = Node("PropertyPlantAndEquipmentGross", attribute="debit", parent=nca1_13_1)
nca2_28_1 = Node("PropertyPlantAndEquipment", attribute="debit", parent=nca2_28) #IFRS
nca2_29 = Node("AccumulatedDepreciationDepletionAndAmortizationPropertyPlantAndEquipment", attribute="credit", parent=nca1_13_1)

nca2_30 = Node("OilAndGasPropertySuccessfulEffortMethodGross", attribute="debit", parent=nca1_16)
nca2_31 = Node("OilAndGasPropertySuccessfulEffortMethodAccumulatedDepreciationDepletionAmortizationAndImpairment", attribute="credit", parent=nca1_16)
nca2_32 = Node("OtherOilAndGasPropertySuccessfulEffortMethod", attribute="debit", parent=nca1_16)

nca2_33 = Node("OilAndGasPropertyFullCostMethodGross", attribute="debit", parent=nca1_17)
nca2_34 = Node("OilAndGasPropertyFullCostMethodDepletion", attribute="credit", parent=nca1_17)

nca2_35 = Node("LongTermInvestments", attribute="debit", parent=nca1_18)
nca2_36 = Node("LongTermAccountsNotesAndLoansReceivableNetNoncurrent", attribute="debit", parent=nca1_18)

nca2_37 = Node("Goodwill", attribute="debit", parent=nca1_19_1)
nca2_38 = Node("IntangibleAssetsNetExcludingGoodwill", attribute="debit", parent=nca1_19_1)
nca2_38_1 = Node("IntangibleAssetsOtherThanGoodwill", attribute="debit", parent=nca2_38)

nca2_39 = Node("PrepaidExpenseOtherNoncurrent", attribute="debit", parent=nca1_20)
nca2_40 = Node("PrepaidMineralRoyaltiesNoncurrent", attribute="debit", parent=nca1_20)

nca2_41 = Node("DerivativeAssetsNoncurrent", attribute="debit", parent=nca1_23)
nca2_42 = Node("HedgingAssetsNoncurrent", attribute="debit", parent=nca1_23)
nca2_43 = Node("CommodityContractAssetNoncurrent", attribute="debit", parent=nca1_23)
nca2_44 = Node("EnergyMarketingContractsAssetsNoncurrent", attribute="debit", parent=nca1_23)

nca2_45 = Node("RegulatoryAssetsNoncurrent", attribute="debit", parent=nca1_24)
nca2_46 = Node("SecuritizedRegulatoryTransitionAssetsNoncurrent", attribute="debit", parent=nca1_24)
nca2_47 = Node("DemandSideManagementProgramCostsNoncurrent", attribute="debit", parent=nca1_24)
nca2_48 = Node("UnamortizedLossReacquiredDebtNoncurrent", attribute="debit", parent=nca1_24)
nca2_49 = Node("DecommissioningFundInvestments", attribute="debit", parent=nca1_24)
nca2_50 = Node("AssetRecoveryDamagedPropertyCostsNoncurrent", attribute="debit", parent=nca1_24)
nca2_51 = Node("DeferredStormAndPropertyReserveDeficiencyNoncurrent", attribute="debit", parent=nca1_24)
nca2_52 = Node("InvestmentsInPowerAndDistributionProjects", attribute="debit", parent=nca1_24)
nca2_53 = Node("UnamortizedDebtIssuanceExpense", attribute="debit", parent=nca1_24)
nca2_54 = Node("PhaseInPlanAmountOfCostsDeferredForRateMakingPurposes", attribute="debit", parent=nca1_24)

nca2_55 = Node("RestrictedCashAndCashEquivalentsNoncurrent", attribute="debit", parent=nca1_28)
nca2_55 = Node("RestrictedInvestmentsNoncurrent", attribute="debit", parent=nca1_28)
nca2_55 = Node("OtherRestrictedAssetsNoncurrent", attribute="debit", parent=nca1_28)

nca2_56 = Node("DisposalGroupIncludingDiscontinuedOperationOtherNoncurrentAssets", attribute="debit", parent=nca1_29)
nca2_57 = Node("DisposalGroupIncludingDiscontinuedOperationInventoryNoncurrent", attribute="debit", parent=nca1_29)
nca2_58 = Node("DisposalGroupIncludingDiscontinuedOperationDeferredTaxAssets", attribute="debit", parent=nca1_29)
nca2_59 = Node("DisposalGroupIncludingDiscontinuedOperationIntangibleAssetsNoncurrent", attribute="debit",
               parent=nca1_29)
nca2_60 = Node("DisposalGroupIncludingDiscontinuedOperationGoodwillNoncurrent", attribute="debit", parent=nca1_29)
nca2_61 = Node("DisposalGroupIncludingDiscontinuedOperationPropertyPlantAndEquipmentNoncurrent", attribute="debit",
               parent=nca1_29)

nca2_62 = Node("DeferredCostsLeasingNetNoncurrent", attribute="debit", parent=nca1_33)
nca2_63 = Node("CapitalizedSoftwareDevelopmentCostsForSoftwareSoldToCustomers", attribute="debit", parent=nca1_33)
nca2_64 = Node("DeferredCompensationPlanAssets", attribute="debit", parent=nca1_33)

nca2_65 = Node("OtherReceivableBeforeAllowanceForCreditLossNoncurrent", attribute="debit", parent=nca1_38)
nca2_66 = Node("OtherReceivableAllowanceForCreditLossNoncurrent", attribute="debit", parent=nca1_38)

# Level 3
nca3_1 = Node("LandAndLandImprovements", attribute="debit", parent=nca2_28_1)
nca3_2 = Node("BuildingsAndImprovementsGross", attribute="debit", parent=nca2_28_1)
nca3_3 = Node("MachineryAndEquipmentGross", attribute="debit", parent=nca2_28_1)
nca3_4 = Node("FurnitureAndFixturesGross", attribute="debit", parent=nca2_28_1)
nca3_5 = Node("FixturesAndEquipmentGross", attribute="debit", parent=nca2_28_1)
nca3_6 = Node("CapitalizedComputerSoftwareGross", attribute="debit", parent=nca2_28_1)
nca3_7 = Node("ConstructionInProgressGross", attribute="debit", parent=nca2_28_1)
nca3_8 = Node("LeaseholdImprovementsGross", attribute="debit", parent=nca2_28_1)
nca3_9 = Node("TimberAndTimberlands", attribute="debit", parent=nca2_28_1)
nca3_10 = Node("PropertyPlantAndEquipmentOther", attribute="debit", parent=nca2_28_1)

nca3_11 = Node("UnprovedOilAndGasPropertySuccessfulEffortMethod", attribute="debit", parent=nca2_30)
nca3_12 = Node("ProvedOilAndGasPropertySuccessfulEffortMethod", attribute="debit", parent=nca2_30)

nca3_13 = Node("OilAndGasPropertySuccessfulEffortMethodAccumulatedImpairment", attribute="credit", parent=nca2_31)
nca3_14 = Node("OilAndGasPropertySuccessfulEffortMethodAccumulatedDepreciationDepletionAndAmortization",
               attribute="credit", parent=nca2_31)

nca3_15 = Node("InvestmentsInAffiliatesSubsidiariesAssociatesAndJointVentures", attribute="debit", parent=nca2_35)
nca3_16 = Node("EquitySecuritiesFVNINoncurrent", attribute="debit", parent=nca2_35)
nca3_17 = Node("DebtSecuritiesNoncurrent", attribute="debit", parent=nca2_35)
nca3_18 = Node("MarketableSecuritiesNoncurrent", attribute="debit", parent=nca2_35)
nca3_19 = Node("InvestmentInPhysicalCommodities", attribute="debit", parent=nca2_35)
nca3_20 = Node("OtherLongTermInvestments", attribute="debit", parent=nca2_35)
nca3_21 = Node("AuctionRateSecuritiesNoncurrent", attribute="debit", parent=nca2_35)
nca3_22 = Node("LeveragedLeaseInvestment", attribute="debit", parent=nca2_35)

nca3_23 = Node("AccountsReceivableNetNoncurrent", attribute="debit", parent=nca2_36)
nca3_24 = Node("NotesAndLoansReceivableNetNoncurrent", attribute="debit", parent=nca2_36)

nca3_25 = Node("GoodwillGross", attribute="debit", parent=nca2_37)
nca3_26 = Node("GoodwillImpairedAccumulatedImpairmentLoss", attribute="credit", parent=nca2_37)

nca3_27 = Node("FiniteLivedIntangibleAssetsNet", attribute="debit", parent=nca2_38)
nca3_28 = Node("IndefiniteLivedIntangibleAssetsExcludingGoodwill", attribute="debit", parent=nca2_38)
nca3_29 = Node("OtherIntangibleAssetsNet", attribute="debit", parent=nca2_38)

nca3_30 = Node("RestrictedCashNoncurrent", attribute="debit", parent=nca2_55)
nca3_31 = Node("RestrictedCashEquivalentsNoncurrent", attribute="debit", parent=nca2_55)

# Level 4

nca4_1 = Node("EquityMethodInvestments", attribute="debit", parent=nca3_15)
nca4_2 = Node("AdvancesToAffiliate", attribute="debit", parent=nca3_15)

nca4_3 = Node("AvailableForSaleSecuritiesDebtSecuritiesNoncurrent", attribute="debit", parent=nca3_17)
nca4_4 = Node("DebtSecuritiesHeldToMaturityAmortizedCostAfterAllowanceForCreditLossNoncurrent", attribute="debit",
              parent=nca3_17)

nca4_5 = Node("AccountsReceivableGrossNoncurrent", attribute="debit", parent=nca3_23)
nca4_6 = Node("AllowanceForDoubtfulAccountsReceivableNoncurrent", attribute="credit", parent=nca3_23)

nca4_7 = Node("NotesAndLoansReceivableGrossNoncurrent", attribute="debit", parent=nca3_24)
nca4_8 = Node("AllowanceForNotesAndLoansReceivableNoncurrent", attribute="credit", parent=nca3_24)

nca4_9 = Node("FiniteLivedIntangibleAssetsAccumulatedAmortization", attribute="credit", parent=nca3_27)
nca4_10 = Node("FiniteLivedIntangibleAssetsGross", attribute="debit", parent=nca3_27)

# Level 5

nca5_1 = Node("HeldToMaturitySecuritiesNoncurrent", attribute="debit", parent=nca4_4)
nca5_2 = Node("DebtSecuritiesHeldToMaturityAllowanceForCreditLossNoncurrent", attribute="credit", parent=nca4_4)

nca5_3 = Node("ConstructionContractorReceivableIncludingContractRetainageAfterYearOne", attribute="debit",
              parent=nca4_5)
nca5_4 = Node("ConstructionContractorReceivableRetainageAfterYearOne", attribute="debit", parent=nca4_5)
nca5_5 = Node("ContractReceivableDueAfterOneYear", attribute="debit", parent=nca4_5)

"""
Current Liabilities
"""
cl1 = Node("CurrentLiabilities", attribute="credit", parent=l)
cl = Node("LiabilitiesCurrent", attribute="credit", parent=cl1)

# Level 1

cl1_1 = Node("AccountsPayableAndAccruedLiabilitiesCurrent", attribute="credit", parent=cl)
cl1_1_1 = Node("CurrentAccrualsAndCurrentDeferredIncomeIncludingCurrentContractLiabilities", attribute = "credit", parent = cl1_1) # IFRS
cl1_2 = Node("DeferredRevenueCurrent", attribute="credit", parent=cl)
cl1_3 = Node("DebtCurrent", attribute="credit", parent=cl)
cl1_4 = Node("DeferredCompensationLiabilityCurrent", attribute="credit", parent=cl)
cl1_5 = Node("DeferredRentCreditCurrent", attribute="credit", parent=cl)
cl1_6 = Node("DerivativeInstrumentsAndHedgesLiabilities", attribute="credit", parent=cl)
cl1_7 = Node("RestructuringReserveCurrent", attribute="credit", parent=cl)
cl1_8 = Node("LiabilityForUncertainTaxPositionsCurrent", attribute="credit", parent=cl)
cl1_9 = Node("PostemploymentBenefitsLiabilityCurrent", attribute="credit", parent=cl)
cl1_10 = Node("SecuritiesLoaned", attribute="credit", parent=cl)
cl1_11 = Node("RegulatoryLiabilityCurrent", attribute="credit", parent=cl)
cl1_12 = Node("ProvisionForLossOnContracts", attribute="credit", parent=cl)
cl1_13 = Node("LitigationReserveCurrent", attribute="credit", parent=cl)
cl1_14 = Node("AccruedEnvironmentalLossContingenciesCurrent", attribute="credit", parent=cl)
cl1_15 = Node("AssetRetirementObligationCurrent", attribute="credit", parent=cl)
cl1_16 = Node("AccruedCappingClosurePostClosureAndEnvironmentalCosts", attribute="credit", parent=cl)
cl1_17 = Node("AccruedReclamationCostsCurrent", attribute="credit", parent=cl)
cl1_18 = Node("DeferredGasPurchasesCurrent", attribute="credit", parent=cl)
cl1_19 = Node("DueToRelatedPartiesCurrent", attribute="credit", parent=cl)
cl1_20 = Node("LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationCurrent", attribute="credit", parent=cl)
cl1_21 = Node("LiabilitiesOfBusinessTransferredUnderContractualArrangementCurrent", attribute="credit", parent=cl)
cl1_22 = Node("SharesSubjectToMandatoryRedemptionSettlementTermsAmountCurrent", attribute="credit", parent=cl)
cl1_23 = Node("CustomerRefundLiabilityCurrent", attribute="credit", parent=cl)
cl1_24 = Node("SelfInsuranceReserveCurrent", attribute="credit", parent=cl)
cl1_25 = Node("ProgramRightsObligationsCurrent", attribute="credit", parent=cl)
cl1_26 = Node("BusinessCombinationContingentConsiderationLiabilityCurrent", attribute="credit", parent=cl)
cl1_27 = Node("OtherLiabilitiesCurrent", attribute="credit", parent=cl)

# Level 2

cl2_1 = Node("AccountsPayableCurrent", attribute="credit", parent=cl1_1_1)
cl2_2 = Node("AccruedLiabilitiesCurrent", attribute="credit", parent=cl1_1_1)
cl2_3 = Node("EmployeeRelatedLiabilitiesCurrent", attribute="credit", parent=cl1_1_1)
cl2_4 = Node("TaxesPayableCurrent", attribute="credit", parent=cl1_1_1)
cl2_5 = Node("InterestAndDividendsPayableCurrent", attribute="credit", parent=cl1_1_1)
cl2_6 = Node("SettlementLiabilitiesCurrent", attribute="credit", parent=cl1_1_1)

cl2_7 = Node("ContractWithCustomerLiabilityCurrent", attribute="credit", parent=cl1_2)
cl2_8 = Node("DeferredIncomeCurrent", attribute="credit", parent=cl1_2)

cl2_9 = Node("ShortTermBorrowings", attribute="credit", parent=cl1_3)
cl2_10 = Node("LongTermDebtAndCapitalLeaseObligationsCurrent", attribute="credit", parent=cl1_3)
cl2_29 = Node("ShorttermBorrowings", attribute="credit", parent=cl1_3)
cl2_30 = Node("CurrentPortionOfLongtermBorrowings", attribute="credit", parent=cl1_3)
cl2_31 = Node("CurrentBorrowingsAndCurrentPortionOfNoncurrentBorrowings", attribute="credit", parent=cl1_3)

cl2_11 = Node("DeferredCompensationShareBasedArrangementsLiabilityCurrent", attribute="credit", parent=cl1_4)
cl2_12 = Node("DeferredCompensationCashBasedArrangementsLiabilityCurrent", attribute="credit", parent=cl1_4)
cl2_13 = Node("OtherDeferredCompensationArrangementsLiabilityCurrent", attribute="credit", parent=cl1_4)

cl2_14 = Node("DerivativeLiabilitiesCurrent", attribute="credit", parent=cl1_6)
cl2_15 = Node("EnergyMarketingContractLiabilitiesCurrent", attribute="credit", parent=cl1_6)
cl2_16 = Node("HedgingLiabilitiesCurrent", attribute="credit", parent=cl1_6)

cl2_17 = Node("AccountsPayableRelatedPartiesCurrent", attribute="credit", parent=cl1_19)
cl2_18 = Node("NotesPayableRelatedPartiesClassifiedCurrent", attribute="credit", parent=cl1_19)
cl2_19 = Node("DueToEmployeesCurrent", attribute="credit", parent=cl1_19)
cl2_20 = Node("DueToOfficersOrStockholdersCurrent", attribute="credit", parent=cl1_19)
cl2_21 = Node("DueToAffiliateCurrentDueToOtherRelatedPartiesClassifiedCurrent", attribute="credit", parent=cl1_19)
cl2_22 = Node("DueToOtherRelatedPartiesClassifiedCurrent", attribute="credit", parent=cl1_19)

cl2_23 = Node("DisposalGroupIncludingDiscontinuedOperationAccountsPayableAndAccruedLiabilitiesCurrent",attribute="credit", parent=cl1_20)
cl2_24 = Node("DisposalGroupIncludingDiscontinuedOperationDeferredRevenueCurrent", attribute="credit", parent=cl1_20)
cl2_25 = Node("DisposalGroupIncludingDiscontinuedOperationAccruedIncomeTaxesPayable", attribute="credit", parent=cl1_20)
cl2_26 = Node("DisposalGroupIncludingDiscontinuedOperationOtherCurrentLiabilities", attribute="credit", parent=cl1_20)
cl2_27 = Node("DisposalGroupIncludingDiscontinuedOperationPensionPlanBenefitObligationCurrent", attribute="credit", parent=cl1_20)
cl2_28 = Node("DisposalGroupIncludingDiscontinuedOperationPostretirementPlanBenefitObligationCurrent", attribute="credit", parent=cl1_20)

# Level 3

cl3_1 = Node("AccountsPayableTradeCurrent", attribute="credit", parent=cl2_1)
cl3_2 = Node("AccountsPayableInterestBearingCurrent", attribute="credit", parent=cl2_1)
cl3_3 = Node("ConstructionPayableCurrent", attribute="credit", parent=cl2_1)
cl3_4 = Node("OilAndGasSalesPayableCurrent", attribute="credit", parent=cl2_1)
cl3_5 = Node("GasPurchasePayableCurrent", attribute="credit", parent=cl2_1)
cl3_6 = Node("EnergyMarketingAccountsPayable", attribute="credit", parent=cl2_1)
cl3_7 = Node("GasImbalancePayableCurrent", attribute="credit", parent=cl2_1)
cl3_8 = Node("AccountsPayableUnderwritersPromotersAndEmployeesOtherThanSalariesAndWagesCurrent", attribute="credit",parent=cl2_1)
cl3_9 = Node("AccountsPayableOtherCurrent", attribute="credit", parent=cl2_1)
cl3_63= Node("TradeAndOtherCurrentPayablesToRelatedParties", attribute="credit", parent=cl2_1) #IFRS
cl3_64= Node("CurrentContractLiabilities", attribute="credit", parent=cl2_1) #IFRS

cl3_10 = Node("AccruedInsuranceCurrent", attribute="credit", parent=cl2_2)
cl3_11 = Node("AccruedRentCurrent", attribute="credit", parent=cl2_2)
cl3_12 = Node("AccruedRoyaltiesCurrent", attribute="credit", parent=cl2_2)
cl3_13 = Node("AccruedUtilitiesCurrent", attribute="credit", parent=cl2_2)
cl3_14 = Node("AccruedSalesCommissionCurrent", attribute="credit", parent=cl2_2)
cl3_15 = Node("AccruedProfessionalFeesCurrent", attribute="credit", parent=cl2_2)
cl3_16 = Node("AccruedAdvertisingCurrent", attribute="credit", parent=cl2_2)
cl3_17 = Node("AccruedExchangeFeeRebateCurrent", attribute="credit", parent=cl2_2)
cl3_18 = Node("ProductWarrantyAccrualClassifiedCurrent", attribute="credit", parent=cl2_2)
cl3_19 = Node("AccruedMarketingCostsCurrent", attribute="credit", parent=cl2_2)
cl3_20 = Node("OtherAccruedLiabilitiesCurrent", attribute="credit", parent=cl2_2)
cl3_66 = Node("Accruals", attribute="credit", parent=cl2_2) #IFRS
cl3_65 = Node("AccrualsClassifiedAsCurrent", attribute="credit", parent=cl2_2) #IFRS

cl3_21 = Node("AccruedSalariesCurrent", attribute="credit", parent=cl2_3)
cl3_22 = Node("AccruedVacationCurrent", attribute="credit", parent=cl2_3)
cl3_23 = Node("AccruedBonusesCurrent", attribute="credit", parent=cl2_3)
cl3_24 = Node("AccruedPayrollTaxesCurrent", attribute="credit", parent=cl2_3)
cl3_25 = Node("AccruedEmployeeBenefitsCurrent", attribute="credit", parent=cl2_3)
cl3_26 = Node("WorkersCompensationLiabilityCurrent", attribute="credit", parent=cl2_3)
cl3_27 = Node("PensionAndOtherPostretirementDefinedBenefitPlansCurrentLiabilities", attribute="credit", parent=cl2_3)
cl3_28 = Node("PensionAndOtherPostretirementAndPostemploymentBenefitPlansLiabilitiesCurrent", attribute="credit", parent=cl2_3)
cl3_29 = Node("OtherEmployeeRelatedLiabilitiesCurrent", attribute="credit", parent=cl2_3)
cl3_30 = Node("DefinedBenefitPensionPlanLiabilitiesCurrent", attribute="credit", parent=cl2_3)

cl3_31 = Node("SalesAndExciseTaxPayableCurrent", attribute="credit", parent=cl2_4)
cl3_32 = Node("AccruedIncomeTaxesCurrent", attribute="credit", parent=cl2_4)
cl3_33 = Node("AccrualForTaxesOtherThanIncomeTaxesCurrent", attribute="credit", parent=cl2_4)

cl3_34 = Node("DividendsPayableCurrent", attribute="credit", parent=cl2_5)
cl3_35 = Node("InterestPayableCurrent", attribute="credit", parent=cl2_5)

cl3_36 = Node("BankOverdrafts", attribute="credit", parent=cl2_9)
cl3_37 = Node("CommercialPaper", attribute="credit", parent=cl2_9)
cl3_38 = Node("BridgeLoan", attribute="credit", parent=cl2_9)
cl3_39 = Node("ConstructionLoan", attribute="credit", parent=cl2_9)
cl3_40 = Node("ShortTermBankLoansAndNotesPayable", attribute="credit", parent=cl2_9)
cl3_41 = Node("ShortTermNonBankLoansAndNotesPayable", attribute="credit", parent=cl2_9)
cl3_42 = Node("SecuritiesSoldUnderAgreementsToRepurchase", attribute="credit", parent=cl2_9)
cl3_43 = Node("FederalHomeLoanBankAdvancesMaturitiesSummaryDueWithinOneYearOfBalanceSheetDate", attribute="credit",
              parent=cl2_9)
cl3_44 = Node("WarehouseAgreementBorrowings", attribute="credit", parent=cl2_9)
cl3_45 = Node("OtherShortTermBorrowings", attribute="credit", parent=cl2_9)

cl3_46 = Node("SecuredDebtCurrent", attribute="credit", parent=cl2_10)
cl3_47 = Node("ConvertibleDebtCurrent", attribute="credit", parent=cl2_10)
cl3_48 = Node("UnsecuredDebtCurrent", attribute="credit", parent=cl2_10)
cl3_49 = Node("SubordinatedDebtCurrent", attribute="credit", parent=cl2_10)
cl3_50 = Node("ConvertibleSubordinatedDebtCurrent", attribute="credit", parent=cl2_10)
cl3_51 = Node("LongTermCommercialPaperCurrent", attribute="credit", parent=cl2_10)
cl3_52 = Node("LongTermConstructionLoanCurrent", attribute="credit", parent=cl2_10)
cl3_53 = Node("LongtermTransitionBondCurrent", attribute="credit", parent=cl2_10)
cl3_54 = Node("LongtermPollutionControlBondCurrent", attribute="credit", parent=cl2_10)
cl3_55 = Node("JuniorSubordinatedDebentureOwedToUnconsolidatedSubsidiaryTrustCurrent", attribute="credit",
              parent=cl2_10)
cl3_56 = Node("OtherLongTermDebtCurrent", attribute="credit", parent=cl2_10)
cl3_57 = Node("LinesOfCreditCurrent", attribute="credit", parent=cl2_10)
cl3_58 = Node("NotesAndLoansPayableCurrent", attribute="credit", parent=cl2_10)
cl3_59 = Node("SpecialAssessmentBondCurrent", attribute="credit", parent=cl2_10)
cl3_60 = Node("FederalHomeLoanBankAdvancesCurrent", attribute="credit", parent=cl2_10)

cl3_61 = Node("DisposalGroupIncludingDiscontinuedOperationAccountsPayableCurrent", attribute="credit", parent=cl2_23)
cl3_62 = Node("DisposalGroupIncludingDiscontinuedOperationAccruedLiabilitiesCurrent", attribute="credit", parent=cl2_23)

# Level 4

cl4_6 = Node("CurrentAdvances", attribute = "credit", parent = cl3_64)

cl4_1 = Node("StandardProductWarrantyAccrualCurrent", attribute="credit", parent=cl3_18)
cl4_2 = Node("ExtendedProductWarrantyAccrualCurrent", attribute="credit", parent=cl3_18)

cl4_3 = Node("TaxCutsAndJobsActOf2017TransitionTaxForAccumulatedForeignEarningsLiabilityCurrent", attribute="credit",
             parent=cl3_32)

cl4_4 = Node("NotesPayableCurrent", attribute="credit", parent=cl3_58)
cl4_5 = Node("LoansPayableCurrent", attribute="credit", parent=cl3_58)

# Level 5

cl5_1 = Node("MediumtermNotesCurrent", attribute="credit", parent=cl4_4)
cl5_2 = Node("ConvertibleNotesPayableCurrent", attribute="credit", parent=cl4_4)
cl5_3 = Node("NotesPayableToBankCurrent", attribute="credit", parent=cl4_4)
cl5_4 = Node("SeniorNotesCurrent", attribute="credit", parent=cl4_4)
cl5_5 = Node("JuniorSubordinatedNotesCurrent", attribute="credit", parent=cl4_4)
cl5_6 = Node("OtherNotesPayableCurrent", attribute="credit", parent=cl4_4)

cl5_7 = Node("LoansPayableToBankCurrent", attribute="credit", parent=cl4_5)
cl5_8 = Node("OtherLoansPayableCurrent", attribute="credit", parent=cl4_5)

"""
Non-Current Liabilties
"""

ncl = Node("LiabilitiesNoncurrent", attribute="credit", parent=l)
ncl1 = Node("NoncurrentLiabilities", attribute="credit", parent=ncl)

# Level 1

ncl1_1 = Node("LongTermDebtAndCapitalLeaseObligations", attribute="credit", parent=ncl1)
ncl1_2 = Node("LiabilitiesOtherThanLongtermDebtNoncurrent", attribute="credit", parent=ncl1)

# Level 2

ncl2_1 = Node("LongTermDebtNoncurrent", attribute="credit", parent=ncl1_1)
ncl2_2 = Node("CapitalLeaseObligationsNoncurrent", attribute="credit", parent=ncl1_1)

ncl2_3 = Node("LiabilitiesOtherThanLongtermDebtNoncurrent", attribute="credit", parent=ncl1_2)

# Level 3

ncl3_1 = Node("LongTermLineOfCredit", attribute="credit", parent=ncl2_1)
ncl3_2 = Node("CommercialPaperNoncurrent", attribute="credit", parent=ncl2_1)
ncl3_3 = Node("ConstructionLoanNoncurrent", attribute="credit", parent=ncl2_1)
ncl3_4 = Node("SecuredLongTermDebt", attribute="credit", parent=ncl2_1)
ncl3_5 = Node("SubordinatedLongTermDebt", attribute="credit", parent=ncl2_1)
ncl3_6 = Node("UnsecuredLongTermDebt", attribute="credit", parent=ncl2_1)
ncl3_7 = Node("ConvertibleDebtNoncurrent", attribute="credit", parent=ncl2_1)
ncl3_8 = Node("ConvertibleSubordinatedDebtNoncurrent", attribute="credit", parent=ncl2_1)
ncl3_9 = Node("LongTermTransitionBond", attribute="credit", parent=ncl2_1)
ncl3_10 = Node("LongTermPollutionControlBond", attribute="credit", parent=ncl2_1)
ncl3_11 = Node("JuniorSubordinatedDebentureOwedToUnconsolidatedSubsidiaryTrustNoncurrent", attribute="credit", parent=ncl2_1)
ncl3_12 = Node("LongTermNotesAndLoans", attribute="credit", parent=ncl2_1)
ncl3_13 = Node("SpecialAssessmentBondNoncurrent", attribute="credit", parent=ncl2_1)
ncl3_14 = Node("LongtermFederalHomeLoanBankAdvancesNoncurrent", attribute="credit", parent=ncl2_1)
ncl3_15 = Node("OtherLongTermDebtNoncurrent", attribute="credit", parent=ncl2_1)
ncl3_45 = Node("LongtermBorrowings", attribute="credit", parent=ncl2_1)

ncl3_16 = Node("AccountsPayableAndAccruedLiabilitiesNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_17 = Node("DeferredRevenueNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_18 = Node("DeferredCompensationLiabilityClassifiedNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_19 = Node("AccumulatedDeferredInvestmentTaxCredit", attribute="credit", parent=ncl2_3)
ncl3_20 = Node("DeferredGainOnSaleOfProperty", attribute="credit", parent=ncl2_3)
ncl3_21 = Node("DeferredRentCreditNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_22 = Node("AssetRetirementObligationsNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_23 = Node("DeferredIncomeTaxLiabilitiesNet", attribute="credit", parent=ncl2_3)
ncl3_24 = Node("LiabilityForUncertainTaxPositionsNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_25 = Node("PensionAndOtherPostretirementAndPostemploymentBenefitPlansLiabilitiesNoncurrent", attribute="credit",
               parent=ncl2_3)
ncl3_26 = Node("AccruedEnvironmentalLossContingenciesNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_27 = Node("CustomerRefundLiabilityNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_28 = Node("OffMarketLeaseUnfavorable", attribute="credit", parent=ncl2_3)
ncl3_29 = Node("LeaseDepositLiability", attribute="credit", parent=ncl2_3)
ncl3_30 = Node("SharesSubjectToMandatoryRedemptionSettlementTermsAmountNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_31 = Node("LitigationReserveNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_32 = Node("RegulatoryLiabilityNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_33 = Node("RestructuringReserveNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_34 = Node("DueToRelatedPartiesNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_35 = Node("LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_36 = Node("LiabilitiesOfBusinessTransferredUnderContractualArrangementNoncurrent", attribute="credit",
               parent=ncl2_3)
ncl3_37 = Node("OtherLiabilitiesNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_38 = Node("OperatingLeaseLiabilityNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_39 = Node("DueToRelatedPartiesNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_40 = Node("SelfInsuranceReserveNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_41 = Node("ProgramRightsObligationsNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_42 = Node("BusinessCombinationContingentConsiderationLiabilityNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_43 = Node("DerivativeInstrumentsAndHedgesLiabilitiesNoncurrent", attribute="credit", parent=ncl2_3)
ncl3_44 = Node("QualifiedAffordableHousingProjectInvestmentsCommitment", attribute="credit", parent=ncl2_3)

# Level 4

ncl4_1 = Node("LongTermNotesPayable", attribute="credit", parent=ncl3_12)
ncl4_2 = Node("LongTermLoansPayable", attribute="credit", parent=ncl3_12)

ncl4_3 = Node("AccruedInsuranceNoncurrent", attribute="credit", parent=ncl3_16)
ncl4_4 = Node("AccruedIncomeTaxesNoncurrent", attribute="credit", parent=ncl3_16)
ncl4_5 = Node("AccruedRentNoncurrent", attribute="credit", parent=ncl3_16)
ncl4_6 = Node("ProductWarrantyAccrualNoncurrent", attribute="credit", parent=ncl3_16)
ncl4_7 = Node("AccountsPayableInterestBearingNoncurrent", attribute="credit", parent=ncl3_16)
ncl4_8 = Node("OtherAccruedLiabilitiesNoncurrent", attribute="credit", parent=ncl3_16)
ncl4_9 = Node("WorkersCompensationLiabilityNoncurrent", attribute="credit", parent=ncl3_16)

ncl4_10 = Node("ContractWithCustomerLiabilityNoncurrent", attribute="credit", parent=ncl3_17)
ncl4_11 = Node("DeferredIncomeNoncurrent", attribute="credit", parent=ncl3_17)

ncl4_12 = Node("DeferredCompensationSharebasedArrangementsLiabilityClassifiedNoncurrent", attribute="credit",
               parent=ncl3_18)
ncl4_13 = Node("DeferredCompensationCashbasedArrangementsLiabilityClassifiedNoncurrent", attribute="credit",
               parent=ncl3_18)
ncl4_14 = Node("OtherDeferredCompensationArrangementsLiabilityClassifiedNoncurrent", attribute="credit", parent=ncl3_18)

ncl4_15 = Node("MineReclamationAndClosingLiabilityNoncurrent", attribute="credit", parent=ncl3_22)
ncl4_16 = Node("OilAndGasReclamationLiabilityNoncurrent", attribute="credit", parent=ncl3_22)
ncl4_17 = Node("AccruedCappingClosurePostClosureAndEnvironmentalCostsNoncurrent", attribute="credit", parent=ncl3_22)
ncl4_18 = Node("DecommissioningLiabilityNoncurrent", attribute="credit", parent=ncl3_22)
ncl4_19 = Node("SpentNuclearFuelObligationNoncurrent", attribute="credit", parent=ncl3_22)

ncl4_20 = Node("PensionAndOtherPostretirementDefinedBenefitPlansLiabilitiesNoncurrent", attribute="credit",
               parent=ncl3_25)
ncl4_21 = Node("PostemploymentBenefitsLiabilityNoncurrent", attribute="credit", parent=ncl3_25)

ncl4_22 = Node("NotesPayableRelatedPartiesNoncurrent", attribute="credit", parent=ncl3_34)
ncl4_23 = Node("DueToEmployeesNoncurrent", attribute="credit", parent=ncl3_34)
ncl4_24 = Node("DueToOfficersOrStockholdersNoncurrent", attribute="credit", parent=ncl3_34)
ncl4_25 = Node("DueToAffiliateNoncurrent", attribute="credit", parent=ncl3_34)
ncl4_26 = Node("DueToOtherRelatedPartiesNoncurrent", attribute="credit", parent=ncl3_34)
ncl4_27 = Node("AccountsPayableRelatedPartiesNoncurrent", attribute="credit", parent=ncl3_34)

ncl4_28 = Node("DisposalGroupIncludingDiscontinuedOperationDeferredTaxLiabilities", attribute="credit", parent=ncl3_35)
ncl4_29 = Node("DisposalGroupIncludingDiscontinuedOperationDeferredRevenueNoncurrent", attribute="credit",
               parent=ncl3_35)
ncl4_30 = Node("DisposalGroupIncludingDiscontinuedOperationOtherNoncurrentLiabilities", attribute="credit",
               parent=ncl3_35)
ncl4_31 = Node("DisposalGroupIncludingDiscontinuedOperationPensionPlanBenefitObligationNoncurrent", attribute="credit",
               parent=ncl3_35)
ncl4_32 = Node("DisposalGroupIncludingDiscontinuedOperationPostretirementPlanBenefitObligationNoncurrent",
               attribute="credit", parent=ncl3_35)
ncl4_33 = Node("DisposalGroupIncludingDiscontinuedOperationAccruedIncomeTaxPayableNoncurrent", attribute="credit",
               parent=ncl3_35)

ncl4_34 = Node("DerivativeLiabilitiesNoncurrent", attribute="credit", parent=ncl3_43)
ncl4_35 = Node("HedgingLiabilitiesNoncurrent", attribute="credit", parent=ncl3_43)
ncl4_36 = Node("EnergyMarketingContractLiabilitiesNoncurrent", attribute="credit", parent=ncl3_43)

# Level 5

ncl5_1 = Node("MediumtermNotesNoncurrent", attribute="credit", parent=ncl4_1)
ncl5_2 = Node("JuniorSubordinatedLongTermNotes", attribute="credit", parent=ncl4_1)
ncl5_3 = Node("SeniorLongTermNotes", attribute="credit", parent=ncl4_1)
ncl5_4 = Node("ConvertibleLongTermNotesPayable", attribute="credit", parent=ncl4_1)
ncl5_5 = Node("NotesPayableToBankNoncurrent", attribute="credit", parent=ncl4_1)
ncl5_6 = Node("OtherLongTermNotesPayable", attribute="credit", parent=ncl4_1)

ncl5_7 = Node("LongTermLoansFromBank", attribute="credit", parent=ncl4_2)
ncl5_8 = Node("OtherLoansPayableLongTerm", attribute="credit", parent=ncl4_2)

ncl5_9 = Node("TaxCutsAndJobsActOf2017TransitionTaxForAccumulatedForeignEarningsLiabilityNoncurrent",
              attribute="credit", parent=ncl4_4)

ncl5_10 = Node("ExtendedProductWarrantyAccrualNoncurrent", attribute="credit", parent=ncl4_6)
ncl5_11 = Node("StandardProductWarrantyAccrualNoncurrent", attribute="credit", parent=ncl4_6)

ncl5_12 = Node("DefinedBenefitPensionPlanLiabilitiesNoncurrent", attribute="credit", parent=ncl4_20)
ncl5_13 = Node("OtherPostretirementDefinedBenefitPlanLiabilitiesNoncurrent", attribute="credit", parent=ncl4_20)
ncl5_14 = Node("OtherPostretirementBenefitsPayableNoncurrent", attribute="credit", parent=ncl4_20)

"""
Commitments and Contingencies
"""

cc = Node("CommitmentsAndContingencies", attribute="credit")

"""
Temporary Equity
"""

te = Node("TemporaryEquityCarryingAmountIncludingPortionAttributableToNoncontrollingInterests", attribute="credit")

# Level 1

te1_1 = Node("TemporaryEquityCarryingAmountAttributableToParent", attribute="credit", parent=te)
te1_2 = Node("RedeemableNoncontrollingInterestEquityCarryingAmount", attribute="credit", parent=te)

# Level 2
te1_3 = Node("RedeemableNoncontrollingInterestEquityCommonCarryingAmount", attribute="credit", parent=te1_2)
te1_4 = Node("RedeemableNoncontrollingInterestEquityPreferredCarryingAmount", attribute="credit", parent=te1_2)
te1_5 = Node("RedeemableNoncontrollingInterestEquityOtherCarryingAmount", attribute="credit", parent=te1_2)

"""
Stockholder's Equity
"""

se = Node("StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest", attribute="credit")
se1 = Node("Equity", attribute="credit", parent=se)
# Level 1

se1_1 = Node("StockholdersEquity", attribute="credit", parent=se1)
se1_2 = Node("MinorityInterest", attribute="credit", parent=se1)

# Level 2
se2_1 = Node("PreferredStockValue", attribute="credit", parent=se1_1)
se2_2 = Node("PreferredStockSharesSubscribedButUnissuedSubscriptionsReceivable", attribute="debit", parent=se1_1)
se2_3 = Node("CommonStockValue", attribute="credit", parent=se1_1)
se2_27 = Node("IssuedCapital", attribute="credit", parent=se2_3) #IFRS
se2_4 = Node("TreasuryStockValue", attribute="debit", parent=se1_1)
se2_5 = Node("CommonStockHeldBySubsidiary", attribute="debit", parent=se1_1)
se2_6 = Node("CommonStockShareSubscribedButUnissuedSubscriptionsReceivable", attribute="debit", parent=se1_1)
se2_7 = Node("CommonStockSharesSubscriptions", attribute="credit", parent=se1_1)
se2_8 = Node("AdditionalPaidInCapital", attribute="credit", parent=se1_1)
se2_28 = Node("SharePremium", attribute="credit", parent=se2_8) #IFRS
se2_9 = Node("TreasuryStockDeferredEmployeeStockOwnershipPlan", attribute="credit", parent=se1_1)
se2_10 = Node("DeferredCompensationEquity", attribute="debit", parent=se1_1)
se2_11 = Node("AccumulatedOtherComprehensiveIncomeLossNetOfTax", attribute="credit", parent=se1_1)
se2_30 = Node("AccumulatedOtherComprehensiveIncome", attribute="credit", parent=se2_11)
se2_12 = Node("RetainedEarningsAccumulatedDeficit", attribute="credit", parent=se1_1)
se2_26 = Node("RetainedEarnings", attribute="credit", parent=se2_12) #IFRS
se2_13 = Node("UnearnedESOPShares", attribute="debit", parent=se1_1)
se2_14 = Node("OtherAdditionalCapital", attribute="credit", parent=se1_1)
se2_29 = Node("OtherReserves", attribute="credit", parent=se2_14) #IFRS
se2_15 = Node("ReceivableFromOfficersAndDirectorsForIssuanceOfCapitalStock", attribute="debit", parent=se1_1)
se2_16 = Node("ReceivableFromShareholdersOrAffiliatesForIssuanceOfCapitalStock", attribute="debit", parent=se1_1)
se2_17 = Node("WarrantsAndRightsOutstanding", attribute="credit", parent=se1_1)
se2_18 = Node("StockholdersEquityNoteSubscriptionsReceivable", attribute="debit", parent=se1_1)

se2_19 = Node("MinorityInterestInLimitedPartnerships", attribute="credit", parent=se1_2)
se2_20 = Node("MinorityInterestInOperatingPartnerships", attribute="credit", parent=se1_2)
se2_21 = Node("MinorityInterestInPreferredUnitHolders", attribute="credit", parent=se1_2)
se2_22 = Node("MinorityInterestInJointVentures", attribute="credit", parent=se1_2)
se2_23 = Node("OtherMinorityInterests", attribute="credit", parent=se1_2)
se2_24 = Node("NonredeemableNoncontrollingInterest", attribute="credit", parent=se1_2)
se2_25 = Node("NoncontrollingInterestInVariableInterestEntity", attribute="credit", parent=se1_2)

# Level 3
se3_1 = Node("TreasuryStockCommonValue", attribute="debit", parent=se2_4)
se3_2 = Node("TreasuryStockPreferredValue", attribute="debit", parent=se2_4)

se3_3 = Node("AdditionalPaidInCapitalCommonStock", attribute="credit", parent=se2_8)
se3_4 = Node("AdditionalPaidInCapitalPreferredStock", attribute="credit", parent=se2_8)

se3_5 = Node("AccumulatedOtherComprehensiveIncomeLossForeignCurrencyTranslationAdjustmentNetOfTax", attribute="credit",
             parent=se2_11)
se3_6 = Node("AccumulatedOtherComprehensiveIncomeLossAvailableForSaleSecuritiesAdjustmentNetOfTax", attribute="credit",
             parent=se2_11)
se3_7 = Node("AociLossCashFlowHedgeCumulativeGainLossAfterTax", attribute="credit", parent=se2_11)
se3_8 = Node("AccumulatedOtherComprehensiveIncomeLossDefinedBenefitPensionAndOtherPostretirementPlansNetOfTax",
             attribute="debit", parent=se2_11)
se3_9 = Node("AccumulatedOtherComprehensiveIncomeLossFinancialLiabilityFairValueOptionAfterTax", attribute="credit",
             parent=se2_11)
se3_10 = Node("AociDerivativeQualifyingAsHedgeExcludedComponentAfterTax", attribute="credit", parent=se2_11)

se3_11 = Node("RetainedEarningsAppropriated", attribute="credit", parent=se2_26)
se3_12 = Node("RetainedEarningsUnappropriated", attribute="credit", parent=se2_26)

# Level 4
se4_1 = Node("DefinedBenefitPlanAccumulatedOtherComprehensiveIncomeNetGainsLossesAfterTax", attribute="credit",
             parent=se3_8)
se4_2 = Node("DefinedBenefitPlanAccumulatedOtherComprehensiveIncomeNetPriorServiceCostCreditAfterTax",
             attribute="debit", parent=se3_8)
se4_3 = Node("DefinedBenefitPlanAccumulatedOtherComprehensiveIncomeNetTransitionAssetsObligationsAfterTax",
             attribute="credit", parent=se3_8)

"""
Cash and Cash Equivalents - Cashflow
"""
# Level 0
cce = Node("CashAndCashEquivalentsPeriodIncreaseDecrease", attribute="debit")


# End-cash position
cce1 = Node("CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", attribute="debit")
cce2 = Node("CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsIncludingDisposalGroupAndDiscontinuedOperations", attribute="debit", parent=cce1)
cce3 = Node("CashAndCashEquivalentsAtCarryingValue", attribute="debit", parent=cce2)
cce4 = Node("CashAndCashEquivalents", attribute="debit", parent=cce3)

# Level 1

cce1_1 = Node("EffectOfExchangeRateOnCashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsIncludingDisposalGroupAndDiscontinuedOperations", attribute="debit", parent=cce)
cce1_3 = Node("EffectOfExchangeRateOnCashAndCashEquivalents", attribute="debit", parent=cce1_1)
cce1_4 = Node("EffectOfExchangeRateChangesOnCashAndCashEquivalents", attribute="debit", parent=cce1_3)

cce1_2 = Node("CashAndCashEquivalentsPeriodIncreaseDecreaseExcludingExchangeRateEffect", attribute="debit", parent=cce)

# Level 2

cce2_1 = Node("EffectOfExchangeRateOnCashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", attribute="debit", parent=cce1_4)
cce2_2 = Node("EffectOfExchangeRateOnCashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsDisposalGroupIncludingDiscontinuedOperations", attribute="debit", parent=cce2_1)

cce2_3 = Node("NetCashProvidedByUsedInOperatingActivities", attribute="debit", parent=cce1_2)
cce2_3_1 = Node("CashFlowsFromUsedInOperatingActivities", attribute="debit", parent=cce2_3)
cce2_4 = Node("NetCashProvidedByUsedInInvestingActivities", attribute="debit", parent=cce1_2)
cce2_4_1 = Node("CashFlowsFromUsedInInvestingActivities", attribute="debit", parent=cce2_4)
cce2_5 = Node("NetCashProvidedByUsedInFinancingActivities", attribute="debit", parent=cce1_2)
cce2_5_1 = Node("CashFlowsFromUsedInFinancingActivities", attribute="debit", parent=cce2_5)

# Level 3

cce3_7 = Node("EffectOfExchangeRateOnCashAndCashEquivalentsContinuingOperations", attribute="debit", parent=cce2_2)
cce3_8 = Node("EffectOfExchangeRateOnCashAndCashEquivalentsDiscontinuedOperations", attribute="debit", parent=cce2_2)

cce3_1 = Node("ProfitLoss", attribute="debit", parent=cce2_3_1)
cce3_2 = Node("AdjustmentsToReconcileNetIncomeLossToCashProvidedByUsedInOperatingActivities", attribute="debit",
              parent=cce2_3_1)

cce3_3 = Node("NetCashProvidedByUsedInInvestingActivitiesContinuingOperations", attribute="debit", parent=cce2_4_1)
cce3_4 = Node("CashProvidedByUsedInInvestingActivitiesDiscontinuedOperations", attribute="debit", parent=cce2_4_1)

cce3_5 = Node("NetCashProvidedByUsedInFinancingActivitiesContinuingOperations", attribute="debit", parent=cce2_5_1)
cce3_6 = Node("CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations", attribute="debit", parent=cce2_5_1)

# Level 4

cce4_1 = Node("IncomeLossIncludingPortionAttributableToNoncontrollingInterest", attribute="credit", parent=cce3_1)
cce4_2 = Node("IncomeTaxExpenseBenefitContinuingOperationsDiscontinuedOperationsExtraordinaryItems", attribute="debit",
              parent=cce3_1)

cce4_3 = Node("AdjustmentsNoncashItemsToReconcileNetIncomeLossToCashProvidedByUsedInOperatingActivities", attribute="debit", parent=cce3_2)
cce4_4 = Node("PaymentsForProceedsFromTenantAllowance", attribute="credit", parent=cce3_2)
cce4_5 = Node("PaymentsForProceedsFromOtherDeposits", attribute="credit", parent=cce3_2)
cce4_6 = Node("IncreaseDecreaseInOperatingCapital", attribute="credit", parent=cce3_2)
cce4_7 = Node("OtherOperatingActivitiesCashFlowStatement", attribute="debit", parent=cce3_2)

cce4_8 = Node("PaymentsForProceedsFromProductiveAssets", attribute="credit", parent=cce3_3)

# level 5

cce5_1 = Node("PaymentsToAcquireProductiveAssets", attribute="credit", parent=cce4_8)

cce5_2 = Node("DepreciationDepletionAndAmortization", attribute="debit", parent=cce4_3)
cce5_2_1 = Node("DepreciationAndAmortisationExpense", attribute = "debit", parent = cce5_2) #IFRS
cce5_2_2 = Node("DepreciationAmortisationAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss", attribute = "debit", parent = cce5_2_1) #IFRS

# Level 6

cce6_1 = Node("PaymentsToAcquirePropertyPlantAndEquipment", attribute="credit", parent=cce5_1)

cce6_2 = Node("DepreciationAndAmortization", attribute="debit", parent=cce5_2_2)
cce6_3 = Node("Depletion", attribute="debit", parent=cce5_2_2)

# Level 7
cce7_1 = Node("PaymentsToAcquireAndDevelopRealEstate", attribute="credit", parent=cce6_1)
cce7_2 = Node("PaymentsToAcquireFurnitureAndFixtures", attribute="credit", parent=cce6_1)
cce7_3 = Node("PaymentsToAcquireMachineryAndEquipment", attribute="credit", parent=cce6_1)
cce7_4 = Node("PaymentsToAcquireOilAndGasPropertyAndEquipment", attribute="credit", parent=cce6_1)
cce7_5 = Node("PaymentsToExploreAndDevelopOilAndGasProperties", attribute="credit", parent=cce6_1)
cce7_6 = Node("PaymentsToAcquireMiningAssets", attribute="credit", parent=cce6_1)
cce7_7 = Node("PaymentsToAcquireTimberlands", attribute="credit", parent=cce6_1)
cce7_8 = Node("PaymentsToAcquireWaterAndWasteWaterSystems", attribute="credit", parent=cce6_1)
cce7_9 = Node("PaymentsToAcquireOtherPropertyPlantAndEquipment", attribute="credit", parent=cce6_1)

cce7_10 = Node("Depreciation", attribute="debit", parent=cce6_2)
cce7_14 = Node("DepreciationExpense", attribute="debit", parent=cce7_10) #IFRS
cce7_11 = Node("AdjustmentForAmortization", attribute="debit", parent=cce6_2)
cce7_15 = Node("AmortisationExpense", attribute="debit", parent=cce7_11) #IFRS
cce7_12 = Node("AmortizationOfDeferredCharges", attribute="debit", parent=cce6_2)
cce7_13 = Node("OtherDepreciationAndAmortization", attribute="debit", parent=cce6_2)

# Level 8

cce8_1 = Node("PaymentsToAcquireRealEstate", attribute="credit", parent=cce7_1)
cce8_2 = Node("PaymentsToDevelopRealEstateAssets", attribute="credit", parent=cce7_1)
cce8_3 = Node("PaymentsForConstructionInProcess", attribute="credit", parent=cce7_1)

cce8_4 = Node("PaymentsToAcquireOilAndGasProperty", attribute="credit", parent=cce7_4)
cce8_5 = Node("PaymentsToAcquireOilAndGasEquipment", attribute="credit", parent=cce7_4)

cce8_6 = Node("PaymentsToAcquireWaterSystems", attribute="credit", parent=cce7_8)
cce8_7 = Node("PaymentsToAcquireWasteWaterSystems", attribute="credit", parent=cce7_8)

cce8_8 = Node("CostOfGoodsSoldDepreciation", attribute="debit", parent=cce7_14)
cce8_9 = Node("CostOfServicesDepreciation", attribute="debit", parent=cce7_14)
cce8_10 = Node("DepreciationNonproduction", attribute="debit", parent=cce7_14)

cce8_11 = Node("CostOfServicesAmortization", attribute="debit", parent=cce7_15)
cce8_12 = Node("AmortizationOfIntangibleAssets", attribute="debit", parent=cce7_15)
cce8_13 = Node("CostOfGoodsSoldAmortization", attribute="debit", parent=cce7_15)

# Level 9

cce9_1 = Node("PaymentsForDepositsOnRealEstateAcquisitions", attribute="credit", parent=cce8_1)
cce9_2 = Node("PaymentsToAcquireCommercialRealEstate", attribute="credit", parent=cce8_1)
cce9_3 = Node("PaymentsToAcquireBuildings", attribute="credit", parent=cce8_1)
cce9_4 = Node("PaymentsForCapitalImprovements", attribute="credit", parent=cce8_1)
cce9_5 = Node("PaymentsToAcquireResidentialRealEstate", attribute="credit", parent=cce8_1)
cce9_6 = Node("PaymentsToAcquireLand", attribute="credit", parent=cce8_1)
cce9_7 = Node("PaymentsToAcquireLandHeldForUse", attribute="credit", parent=cce8_1)
cce9_8 = Node("PaymentsToAcquireHeldForSaleRealEstate", attribute="credit", parent=cce8_1)
cce9_9 = Node("PaymentsToAcquireOtherRealEstate", attribute="credit", parent=cce8_1)

cce9_10 = Node("", attribute="credit", parent=cce8_1)
