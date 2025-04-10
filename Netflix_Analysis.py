{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "576c5961-be5e-4ca2-80c6-39d44961b297",
   "metadata": {},
   "outputs": [],
   "source": [
    "## Import necessary libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import seaborn as sns\n",
    "import matplotlib.pyplot as plt\n",
    "from collections import Counter\n",
    "from wordcloud import WordCloud\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "cb16bfdf-5483-428c-bd05-3a36350c2803",
   "metadata": {},
   "outputs": [],
   "source": [
    "### Function to check if csv is cleaned\n",
    "\n",
    "file = \"netflix_titles1.csv\"\n",
    "\n",
    "def csv_cleaned_uncleaned(file):\n",
    "    data = pd.read_csv(file)\n",
    "    \n",
    "    missing_val = data.isnull().sum().sum()\n",
    "    duplicate_rows = data.duplicated().sum()\n",
    "    numerical_cols = data.select_dtypes(include=[\"number\"])\n",
    "    outliers = ((numerical_cols - numerical_cols.mean().abs() > 3 * numerical_cols.std()).sum().sum())\n",
    "\n",
    "    # Count number of object type columns (which can be inconsistent if not expected)\n",
    "    invalid_types = sum(data.dtypes == \"object\")\n",
    "\n",
    "    print(f\"Missing Values: \", {missing_val})\n",
    "    print(f\"Duplicate rows \", { duplicate_rows})\n",
    "    print(f\"Outliers \", {outliers})\n",
    "    print(f\"Inconsistent data types\", {invalid_types})\n",
    "\n",
    "    return missing_val == 0 and duplicate_rows == 0 and outliers < 10\n",
    "\n",
    "file_path = \"netflix_titles.csv\"\n",
    "is_clean = csv_cleaned_uncleaned(file)\n",
    "\n",
    "if is_clean :\n",
    "    print(\"The dataset is considered clean !\")\n",
    "else:\n",
    "    print(\"The dataset is  not cleaned !\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e919c47e-b7ef-4646-9479-94fc3ae69b85",
   "metadata": {},
   "source": [
    "#### Load and Inspect the Netflix Dataset"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0675c9ec-1bbb-4fb3-acc6-3686f3f5f74a",
   "metadata": {},
   "outputs": [],
   "source": [
    "## Load CSV file\n",
    "file = \"netflix_titles1.csv\"\n",
    "data = pd.read_csv(file)\n",
    "\n",
    "## Preview the first 6 rows\n",
    "print(\"First 6 rows of the dataset:\")\n",
    "print(data.head(6))\n",
    "\n",
    "## Basic dataset information\n",
    "print(\"Dataset Info:\")\n",
    "print(data.info())\n",
    "\n",
    "## Dataset shape\n",
    "print(\"Dataset Shape:\")\n",
    "print(f\"Rows: {data.shape[0]}, Columns: {data.shape[1]}\")\n",
    "\n",
    "## Check for missing values in each column\n",
    "print(\" Missing Values:\")\n",
    "missing_values = data.isnull().sum()\n",
    "print(missing_values)\n",
    "\n",
    "## Check for duplicate rows\n",
    "duplicate_rows = data.duplicated().sum()\n",
    "print(f\"Duplicate Rows: {duplicate_rows}\")\n",
    "\n",
    "## Descriptive statistics for numerical columns\n",
    "print(\"Summary Statistics:\")\n",
    "summary = data.describe()\n",
    "print(summary)\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "67c3abae-fc61-436b-84f3-e79e726876a9",
   "metadata": {},
   "source": [
    "#### Cleaning CSV file"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "090e9a83-048d-4287-86a1-eeb75da9a301",
   "metadata": {},
   "outputs": [],
   "source": [
    "## Load the dataset\n",
    "data = pd.read_csv('netflix_titles1.csv')  \n",
    "\n",
    "## Standardize different types of missing values\n",
    "missing_cols = ['date_added', 'rating', 'duration']\n",
    "for col in missing_cols:\n",
    "    data[col] = data[col].replace(['none', 'None', '', 'NaN', None], np.nan)\n",
    "\n",
    "## Convert 'date_added' to datetime\n",
    "data['date_added'] = pd.to_datetime(data['date_added'], errors='coerce')\n",
    "\n",
    "## Fill missing values\n",
    "data['director'] = data['director'].fillna('Not specified')\n",
    "data['cast'] = data['cast'].fillna('Not specified')\n",
    "data['country'] = data['country'].fillna('Not specified')\n",
    "\n",
    "\n",
    "\n",
    "if not data['rating'].mode().empty:\n",
    "    data['rating'] = data['rating'].fillna(data['rating'].mode()[0])\n",
    "\n",
    "if not data['duration'].mode().empty:\n",
    "    data['duration'] = data['duration'].fillna(data['duration'].mode()[0])\n",
    "\n",
    "if not data['date_added'].mode().empty:\n",
    "    data['date_added'] = data['date_added'].fillna(data['date_added'].mode()[0])\n",
    "\n",
    "\n",
    "## Create new columns for month and year\n",
    "data['month'] = data['date_added'].dt.month\n",
    "data['year'] = data['date_added'].dt.year\n",
    "\n",
    "## Drop duplicates\n",
    "data.drop_duplicates(inplace=True)\n",
    "\n",
    "## Clean and standardize text columns\n",
    "text_cols = ['type', 'title', 'director', 'cast', 'country', 'rating', 'listed_in', 'description']\n",
    "for col in text_cols:\n",
    "    data[col] = data[col].astype(str).str.strip().str.lower()\n",
    "\n",
    "## Remove old content\n",
    "data = data[data['release_year'] >= 1950]\n",
    "\n",
    "## Split multi-valued columns into lists\n",
    "data['listed_in'] = data['listed_in'].str.replace(r'\\s*,\\s*', ',', regex=True).str.split(',')\n",
    "data['cast'] = data['cast'].str.replace(r'\\s*,\\s*', ',', regex=True).str.split(',')\n",
    "\n",
    "## Final check\n",
    "print(\"Missing values after cleaning:\")\n",
    "print(data.isnull().sum())\n",
    "print(\"\\nDataset preview:\")\n",
    "print(data.head())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 103,
   "id": "dd6ed271-0f94-4c30-8f24-c7a6c7c4fe02",
   "metadata": {},
   "outputs": [],
   "source": [
    "data.to_csv(\"netflix_titles_cleaned.csv\", index = False)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7517bee9-e84a-47f1-acc8-51970e5b088d",
   "metadata": {},
   "source": [
    "#### Content Type Ratio: Movies vs TV Shows"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "71709ed6-5369-4d29-aea2-40fbc83f06c0",
   "metadata": {},
   "outputs": [],
   "source": [
    "## Count how many Movies and TV Shows are in the dataset\n",
    "type_counts = data['type'].value_counts()\n",
    "\n",
    "## Plotting the donut-style pie chart \n",
    "plt.figure(figsize = (6,6))\n",
    "plt.pie(\n",
    "    type_counts,\n",
    "    labels = type_counts.index,\n",
    "    autopct = '%1.1f%%',\n",
    "    startangle = 90,\n",
    "    wedgeprops = {'width': 0.4}\n",
    ")\n",
    "plt.title(\"Content type distribution (Movies vs TV shows)\", fontsize = 13, color = 'darkblue')\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "54e1a60c-06d0-49a6-9bec-8adbefb96a46",
   "metadata": {},
   "source": [
    "#### Genre Richness: Most Popular Genres on Netflix"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "989fbb9f-b6cb-43b4-aed1-da42c67bb392",
   "metadata": {},
   "outputs": [],
   "source": [
    "## Clean and split genre column\n",
    "data['listed_in'] = data['listed_in'].fillna('').astype(str).str.split(', ')\n",
    "genre_list = data['listed_in'].explode().dropna()\n",
    "top_genres = Counter(genre_list)\n",
    "top_genres = dict(sorted(top_genres.items(), key = lambda x : x[1], reverse = True)[:15])\n",
    "\n",
    "## Create DataFrame for plotting\n",
    "genre_df = pd.DataFrame({\n",
    "    'genre' : list(top_genres.values()),\n",
    "    'cast'  : list(top_genres.keys())\n",
    "})\n",
    "\n",
    "### Plotting the top 15 genres\n",
    "plt.figure(figsize = (10,6))\n",
    "sns.barplot(data = genre_df, x='genre', y='cast',  hue='genre', palette='viridis', legend=False, dodge=False)\n",
    "plt.title(\"Top 15 genre's on Netflix\", fontsize= 14, color = \"Darkblue\")\n",
    "plt.xlabel(\"Number of Titles \", fontsize = 12 )\n",
    "plt.ylabel(\"Genre\", fontsize = 10)\n",
    "plt.xticks(fontsize=10)\n",
    "plt.yticks(fontsize=10)\n",
    "plt.subplots_adjust(left=0.3)\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8541f6a5-379e-43c7-8599-0837b91af21b",
   "metadata": {},
   "source": [
    "#### Trend of Releases Over the Years (Movies vs TV Shows)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a2e3a487-5563-4173-8106-13446b6955ec",
   "metadata": {},
   "outputs": [],
   "source": [
    "## reate a stacked histogram by release year and content type\n",
    "plt.figure(figsize=(10, 5))\n",
    "sns.histplot(\n",
    "    data=data,\n",
    "    x='release_year',\n",
    "    hue='type',\n",
    "    multiple='stack',\n",
    "    bins=30,\n",
    "    palette='Set2'\n",
    ")\n",
    "\n",
    "## Customize the chart\n",
    "plt.title(\" Release Year Trend: Movies vs TV Shows\", fontsize=14, color='darkblue')\n",
    "plt.xlabel(\"Release Year\", fontsize=12)\n",
    "plt.ylabel(\"Number of Titles\", fontsize=12)\n",
    "plt.grid(axis='y', linestyle='--', alpha=0.5)\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "546b43c0-f72e-48d6-a87c-85d421c98396",
   "metadata": {},
   "source": [
    "#### Heatmap: Visualizing How Much Content Was Added Over Time (Year vs Month)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "bbdbb26e-cea3-42c9-a98d-3fcb69266dca",
   "metadata": {},
   "outputs": [],
   "source": [
    "## Group the data by year and month to count titles\n",
    "monthly_data = data.groupby(['year', 'month']).size().unstack(fill_value=0)\n",
    "\n",
    "## Plot heatmap \n",
    "plt.figure(figsize=(12,6))\n",
    "sns.heatmap(monthly_data, cmap='YlGnBu')\n",
    "plt.title('Content Added Over Time (Heatmap)')\n",
    "plt.xlabel('Month')\n",
    "plt.ylabel('Year')\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d3922a5c-620f-4579-96c9-69369201fa8e",
   "metadata": {},
   "source": [
    "#### Top 10 Directors and Actors based on number of titles"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4df14d9b-b20f-47b8-ade2-93a0ca6a75a5",
   "metadata": {},
   "outputs": [],
   "source": [
    "## Get top 10 directors and actors\n",
    "top_directors = data['director'].explode().value_counts().head(10)\n",
    "top_actors = data['cast'].explode().value_counts().head(10)\n",
    "\n",
    "## Plot top directors\n",
    "plt.figure(figsize=(8, 5))\n",
    "top_directors.plot(kind='barh', color='darkblue')\n",
    "plt.xlabel(\"Number of Titles\")\n",
    "plt.title(\"Top 10 Directors on Netflix\")\n",
    "plt.gca().invert_yaxis()  \n",
    "plt.show()\n",
    "\n",
    "## Plot top actors\n",
    "plt.figure(figsize=(8, 5))\n",
    "top_actors.plot(kind='barh', color='crimson')\n",
    "plt.xlabel(\"Number of Titles\")\n",
    "plt.title(\"Top 10 Actors on Netflix\")\n",
    "plt.gca().invert_yaxis()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "73a6362f-6e62-4687-a42a-90ab5dd7d082",
   "metadata": {},
   "source": [
    "#### Word Cloud: Most Frequent Words in Descriptions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0c27c17e-6858-4dd3-ab02-4c42cb390322",
   "metadata": {},
   "outputs": [],
   "source": [
    "## Import and combine all text from the 'description' column (drop any missing values)\n",
    "text = ' '.join(data['description'].dropna().astype(str).str.strip())\n",
    "\n",
    "## Generate the word cloud\n",
    "wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)\n",
    "\n",
    "## Plot the word cloud\n",
    "plt.figure(figsize=(10, 5))\n",
    "plt.imshow(wordcloud, interpolation='bilinear')\n",
    "plt.axis('off')\n",
    "plt.title('Common Words in Netflix Descriptions', color='red', fontsize=15)\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "dcdcb37e-e22c-43f0-ae11-96846b34cffd",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
