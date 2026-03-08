import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df=pd.read_csv("/storage/emulated/0/Download/student_performance_messy.csv")
df=df.drop_duplicates()
df["Age"]=pd.to_numeric(df["Age"],errors="coerce")
df["Age"]=np.abs(df["Age"])
df["Age"]=df["Age"].fillna(df['Age'].median())
df["Age"]=df["Age"].astype(int)
def g(x):
    if x=="Male" or x=="M"or x=="male"or x=="m"or x=="1":
        return "Male"
    if x=="Female" or x== "F"or x=="female"or x=="f" or x=="0":
        return "Female"
def h(x):
    if x>100:
        return (x-100)
    if x<100:
        return x
df["Gender"]=df["Gender"].apply(lambda x:g(x))
df["Gender"]=df["Gender"].str.lstrip()
df["Gender"]=df["Gender"].fillna("Male")
df["MathScore"]=df["MathScore"].str.replace("%","")
df["MathScore"]=pd.to_numeric(df["MathScore"],errors="coerce")
df["MathScore"]=df["MathScore"].apply(lambda x:h(x))
df["MathScore"]=(df["MathScore"].fillna(df["MathScore"].mean())).round(1)
df["ScienceScore"]=df["ScienceScore"].str.replace("%","")
df["ScienceScore"]=pd.to_numeric(df["ScienceScore"],errors="coerce")
df["ScienceScore"]=df["ScienceScore"].apply(lambda x:h(x))
df["ScienceScore"]=(df["ScienceScore"].fillna(df["ScienceScore"].mean())).round(1)
df["EnglishScore"]=df["EnglishScore"].str.replace("%","")
df["EnglishScore"]=pd.to_numeric(df["EnglishScore"],errors="coerce")
df["EnglishScore"]=df["EnglishScore"].apply(lambda x:h(x))
df["EnglishScore"]=(df["EnglishScore"].fillna(df["EnglishScore"].mean())).round(1)
df["Department"]=df["Department"].str.lower().str.capitalize()
def j(x):
    if x=="Stats":
        return "Statistics"
    elif x=="Comp sci":
        return "Computer science"
    elif x=="Eng.":
        return "Engineering"
    elif x=="Math":
        return "Mathematics"
    else:
        return x
df["Department"]=df["Department"].apply(lambda x: j(x))
df["Department"]=df["Department"].fillna("Mathematics")
def k(x):
    if x>100:
        return(x-int(str(x)[0])*100)
    else:
        return x
df["Attendance(%)"]=df["Attendance(%)"].fillna(df["Attendance(%)"].median())
df["Attendance(%)"]=(df["Attendance(%)"].apply(lambda x:k(x))).round(1)
df["StudyHoursPerWeek"]=df["StudyHoursPerWeek"].fillna(df["StudyHoursPerWeek"].median())
df["Passed"]=df["Passed"].str.lower().str.capitalize()
def l(x):
    if x=="0":
        return "No"
    elif x=="1":
        return "Yes"
    else:
        return x
df["Passed"]=df["Passed"].apply(lambda x:l(x))
df["Passed"]=df["Passed"].fillna("Yes")
math=df.groupby("Department")["MathScore"].sum().reset_index()
english=df.groupby("Department")["EnglishScore"].sum().reset_index()
science=df.groupby("Department")["ScienceScore"].sum().reset_index()
fig=plt.figure(figsize=(9,9))
gs=fig.add_gridspec(2,4)
ax1=fig.add_subplot(gs[0,:2])
ax1.bar(math["Department"],math["MathScore"])
ax1.set_ylabel("TotalScores")
ax1.set_title("MathScoreDistribution",color="r")
plt.xticks(rotation=90)
ax2=fig.add_subplot(gs[0,2:])
ax2.bar(english["Department"],english["EnglishScore"])
ax2.set_ylabel("TotalScores")
ax2.set_title("EnglishScoreDistribution",color="r")
plt.xticks(rotation=90)
ax3=fig.add_subplot(gs[1,:2])
ax3.bar(science["Department"],science["ScienceScore"])
ax3.set_ylabel("TotalScores")
ax3.set_title("ScienceScoreDistribution",color="r")
plt.xticks(rotation=90)
df["WeightedMean"]=(df["MathScore"]*0.4+df["EnglishScore"]*0.25+df["ScienceScore"]*0.35)
corr=df[["StudyHoursPerWeek","Attendance(%)","WeightedMean"]].corr()
ax3=fig.add_subplot(gs[1,2:])
ax3.imshow(corr)
fig.colorbar(ax3.imshow(corr), ax=ax3)
ax3.set_xticks(range(len(corr.columns)), corr.columns, rotation=90)
ax3.set_yticks(range(len(corr.columns)), corr.columns)
plt.tight_layout()
plt.show()
