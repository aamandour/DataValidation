import pandas as pd

# Load the dataset
df = pd.read_csv("employees.csv")

# -------- EXISTENCE ASSERTIONS --------
# Original: name must not be null
missing_name_count = df['name'].isnull().sum()
print(f"Records with missing 'name': {missing_name_count}")

# New: salary must not be null
missing_salary_count = df['salary'].isnull().sum()
print(f"Records with missing 'salary': {missing_salary_count}")

# -------- LIMIT ASSERTIONS --------
df['hire_date'] = pd.to_datetime(df['hire_date'], errors='coerce')

# Original: hire_date >= 2015
early_hire_count = df[df['hire_date'].dt.year < 2015].shape[0]
print(f"Records hired before 2015: {early_hire_count}")

# New: salary must be between $30k and $200k
salary_violations_count = df[(df['salary'] < 30000) | (df['salary'] > 200000)].shape[0]
print(f"Records with salary out of $30k–$200k range: {salary_violations_count}")

# -------- INTRA-RECORD ASSERTIONS --------
df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')

# Original: birth_date must be before hire_date
invalid_birth_hire = df[df['birth_date'] >= df['hire_date']].shape[0]
print(f"Records where birth_date >= hire_date: {invalid_birth_hire}")

# New: If country is USA, phone must not be null or blank
usa_phone_violations = df[
    (df['country'].str.upper() == 'USA') & 
    (df['phone'].isnull() | (df['phone'].str.strip() == ''))
].shape[0]
print(f"USA employees with missing/blank phone: {usa_phone_violations}")

# -------- INTER-RECORD ASSERTIONS --------
employee_ids = set(df['eid'])
manager_ids = set(df['reports_to'].dropna())
invalid_managers = manager_ids - employee_ids
manager_violations = df[df['reports_to'].isin(invalid_managers)]
print(f"Records with unknown manager ID: {manager_violations.shape[0]}")

# No employee should report to themselves
self_reporting_violations = df[df['eid'] == df['reports_to']]
print(f"Employees who report to themselves: {self_reporting_violations.shape[0]}")

# -------- SUMMARY ASSERTIONS --------
# Each city must have more than one employee
city_counts = df['city'].value_counts()
cities_with_one_employee = city_counts[city_counts == 1]
print(f"Cities with only one employee: {cities_with_one_employee.shape[0]}")

# New Summary Assertion — No postal code should have more than 100 employees
postal_code_counts = df['postal_code'].value_counts()
postal_codes_with_too_many = postal_code_counts[postal_code_counts > 100]
print(f"Postal codes with more than 100 employees: {postal_codes_with_too_many.shape[0]}")

# -------- STATISTICAL ASSERTION: Salaries are normally distributed --------
import matplotlib.pyplot as plt

# Drop missing salary values
salaries = df['salary'].dropna()

# Plot histogram
plt.figure(figsize=(10, 6))
plt.hist(salaries, bins=50, edgecolor='black', alpha=0.7)
plt.title("Histogram of Salaries")
plt.xlabel("Salary")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()

# Save the histogram
plt.savefig("salary_histogram.png")
plt.close()

# Distribution of hire years
hire_year_counts = df['hire_date'].dt.year.value_counts().sort_index()

plt.figure(figsize=(10, 6))
hire_year_counts.plot(kind='bar', edgecolor='black')
plt.title("Distribution of Hire Years")
plt.xlabel("Year")
plt.ylabel("Number of Employees Hired")
plt.grid(True)
plt.tight_layout()
plt.savefig("hire_year_distribution.png")
plt.close()


