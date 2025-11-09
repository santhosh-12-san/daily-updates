
const schoolData = `
{
  "schoolName": "Green Valley High School",
  "location": "Bangalore, India",
  "establishedYear": 1995,
  "teachers": [
    { "id": 1, "name": "Mrs. Priya Sharma", "subject": "Math", "experience": 10 },
    { "id": 2, "name": "Mr. Arjun Reddy", "subject": "Science", "experience": 8 }
  ],
  "students": [
    { "id": 101, "name": "Santhosh H Y", "grade": "10th", "section": "A", "marks": { "math": 85, "science": 90, "english": 88 } },
    { "id": 102, "name": "Ananya R", "grade": "10th", "section": "A", "marks": { "math": 92, "science": 87, "english": 91 } },
    { "id": 103, "name": "Ramesh P", "grade": "10th", "section": "B", "marks": { "math": 70, "science": 75, "english": 80 } }
  ]
}
`;


const school = JSON.parse(schoolData);
console.log('orginal data',school)
console.log(typeof(school))

console.log("School Name:", school.schoolName);
console.log("Location:", school.location);
console.log("----------------------------------");


console.log("All Students (using for loop):");
for (let i = 0; i < school.students.length; i++) {
  const student = school.students[i];
  console.log(`${student.name} - Math: ${student.marks.math}, Science: ${student.marks.science}`);
}

console.log("----------------------------------");

console.log("Students (using forEach):");
school.students.forEach(student => {
  console.log(`${student.name} - English Marks: ${student.marks.english}`);
});
console.log("----------------------------------");

const topScienceStudents = school.students.filter(student => student.marks.science > 85);
console.log("Top Science Students:");
console.log(topScienceStudents);
console.log("----------------------------------");

for (const student of school.students) {
  const marks = student.marks;
  const total = marks.math + marks.science + marks.english;
  const avg = total / 3;
  console.log(`${student.name}'s Average Marks: ${avg.toFixed(2)}`);
}
console.log("----------------------------------");


const jsonString = JSON.stringify(school, null, 2);
console.log("Converted Back to JSON Format:");
console.log(jsonString);
