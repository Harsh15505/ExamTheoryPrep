df.filter((df.age >= 25) & (df.age <= 40)).agg(avg("spending_score").alias("avg_spending_score")).show()
df.filter(mem_year > 5).orderBy(desc("anuual_income")).limit(1).show()1