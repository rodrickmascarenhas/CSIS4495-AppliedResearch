### Setup & Installation

Project was deployed on Google App Engine flexible environment using python 3.7 or higher.
```bash
  https://research-project-4495-387702.uw.r.appspot.com/
```
#### Make sure you have the latest version of Python installed.

Download the GitBash on your local PC
Type and copy-paste the following repository url in place of <repo-url>:<br>
```bash
  git clone <repo-url>
```
Go to folder which has the existing main.py file:<br>
```bash
  python main.py
```
Go to url in the browser:
```bash
  http://127.0.0.1:5000
``` 
 
<h3>Medical Reporting Service Application detecting early skin diseases using Flask, SQLAlchemy and Python</h3>
<ol>
  <li>
    <b>Introduction</b>
    <p>Canada’s Ministry of Youth has allocated enterprise development funds to both the youth and women. Government plans to start entrepreneurial ventures
    that support services for youth in the medical sector. An estimated budget of 4.5B dollars will support the implementation of 801 infrastructure projects
    in British Columbia.</p>
    <p>During recent years, the number of patients who have spent weeks waiting to see a doctor has increased significantly. Fraser Institute says, “a new 
    study shows Canada’s health-care wait times reached 25.6 weeks in 2021—the longest ever recorded—and 175 per cent higher than the 9.3 weeks Canadians 
    waited in 1993”. Services such as medical expert diagnoses and regular checkups are more frequent than we want it to be.</p>
    <div align="center"><img width=380 height=300 src="https://user-images.githubusercontent.com/30309234/208931782-123b7a81-65db-45b5-9d79-1a1714b3173a.png" />
  </div><br>
    <p>We are developing a new application powered by Machine Learning/Artificial intelligence (AI) that can detect various skin diseases known to medical 
    science. Through statistical analyses and predictive models, we can reduce the wait times for patients from the number of weeks to hours through simple
    and easy configuration steps. There is likelihood of risk with early predictions, still more advancements in AI.</p>
    <p>The application will help British Columbians in reducing the amount of time they have to wait to get appointments from specialists. It would be 
    advantageous for the patient to get themselves diagnosed at the early stage so that the disease is curable. Once the user is registered and verified
    successfully, our application will examine the skin-color formation and provide medical solutions accordingly.</p>
  </li>
  <li>
    <b>Project Objectives</b>
    <p>The main objective of this project is to offer people a trusted platform for early detection of potential skin cancer by using Artificial Intelligence
    in Python Language. The users must first log in to access the analysis tool and potentially submit an assessment form to one of our doctors working with our
    platform, then they can either choose to “Check on Our Analysis Tool” or “Chat with a specialist”. For using the analysis tool, the user will be asked to
    answer a questionnaire that would help to improve the prediction accuracy along with uploading a photo of the affected skin area.</p>
    <p>Our Artificial Intelligence (AI) will predict and provide a result based on what type of skin cancer the user might have and is powerful enough to detect
    the differences in moles, scratch, scabs or skin cancer, therefore, the outcome is highly accurate. In addition, the description is included for each of the
    seven classes of skin lesions that will be displayed when the user hovers over the question mark icon. This enables users to understand more about the
    pigmentation, whether it is benign or malignant skin formation, what early signs of benign or malignant lesions could be if they are validated by
    dermatopathologists. Additionally, there is a chatbot which would help to answer the most frequently asked questions from visitors, thus easing the stress
    of customer support on human operatives and instead they can focus on assisting the current customers.</p>
  </li>
  <li>
    <b>Virtual Assistant (Chatbot)</b>
    <p><ul>
    <li>Load dataset and create variables to store patterns and tags.</li>
    <li>Using lemmatizer can effectively analyze synonym words for better chatbot training.</li>
    <li>Creating a Bag-of-Word model to group words with similar meaning together.</li>
    <li>Neural Network Model and training the model.</li>
    <li>Pre-processing the user’s input.</li>
    <li>Now let's call the chatbot and the results are the first screenshots.</li>
    </ul></p>
  </li>
  <li>
    <b>Analysis Tool</b>
    <p>Successfully built a neural network model capable of doing predictions over new, unobserved image files. We’re using Jupyter notebook to develop code for
    our application which will be converted into a .hdf5 file suitable for Flask to handle. Below, we have the source and structure of the model’s configuration:
    <a href="https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T">Harvard Datasets</a></p>
    <p><div align="center"><img width=380 height=300 src="https://user-images.githubusercontent.com/30309234/208763727-c8cb4a3e-a057-465d-a6c9-a320c187f84a.png" />
    </div></p>
    There appears to be no difference between male and female cancer formations over the skin.
    <p><div align="center"><img width=300 height=300 src="https://user-images.githubusercontent.com/30309234/208763825-143f2a6b-641f-421d-86a4-a8d0e8132099.png" />
    </div></p>
    More than 50% of lesions are confirmed through histopathology (histo), the ground truth for the rest of the cases is either follow-up examination (followup),
    expert consensus (consensus), or confirmation by in-vivo confocal microscopy (confocal).
    <p><div align="center"><img width=300 height=300 src="https://user-images.githubusercontent.com/30309234/208764423-736c8aa3-ea24-452c-aa62-924ba9f35727.png" />
    </div></p>
    <p>Patients of ages between 30 and 60 makeup 68% of all cases recorded in skin diseases. Images will be added to user's forms.</p>
  </li>
  <li>
    <b>Software Design Architecture</b>
    <ul>
    <li>UML Diagram
      <p><div align="center"><img src="https://user-images.githubusercontent.com/30309234/208759427-8b53c067-489f-4bd7-88ce-aa89a0993629.png" />
      </div></p></li>
    <li>Sequence Diagram<p><div align="center"><img src="https://user-images.githubusercontent.com/30309234/208931367-53b0abc9-5bc8-4e15-b6bb-c5a4f8ee47aa.png" />
      </div></p></li>
      <li>User Friendly Experience<br>
    <p>A user-friendly website should satisfy the needs and expectations of its targeted audience. These pages ought to offer workable technological solutions that
    the audience expects. There are 5 factors that access the quality of website in terms of user-friendly behavior: Learnability, Efficiency, Memorability,
    Errors, Satisfaction</p>
    <p>Our prediction model was constructed using Keras. Our model ended up offering really excellent accuracy and assisting in delivering fairly decent outcomes.
    When forecasting the outcomes of various skin diseases, our model showed to be 72% accurate</p>
    </li>
    <li>Prediction Accuracy<br>
    <p>Although not a wide range of users have tested the website's interface. We have made an effort to create an interface that is simple enough for most users
    to grasp. In order to quickly steer the user to the route he desires and help him achieve his goals, we have used simple icons and a template framework.
    For e.g., We select symbols that make navigation simple for the user and make it	clear ahead of time what the user will be doing. The user won't have to spend
    much time debugging our programme as a result.</p>
    <p><div align="center"><img width=300 height=300 src="https://user-images.githubusercontent.com/30309234/208942434-39c8f646-0cc8-4755-99c1-0498838043b1.png" />
    </div></p>
    </li>
    <li>Risk Assessment Accuracy<br>
    <p>The core principle of our online application is our Risk Assessment Accuracy tool. The user uploads a picture to be tested, and our model built with Keras
    is runned down depending on that analysis. After that, we are given information on the many types of skin cancer that the photograph may show. Additionally,
    it displays the likelihood(probability)  as well as a brief summary of the specific form of skin cancer and its features.</p>
    <p><div align="center"><img src="https://user-images.githubusercontent.com/30309234/208937664-b0def808-c4f2-489d-8f17-1ce7818c2399.png" />
    </div></p>
    </li>
    <li>What are the benefits of using Flask?<br>
    <p>Flask framework was chosen for this project as it is a lightweight web application framework designed to make getting started quick and easy, with the
    ability to scale up to complex applications. It offers a collection of libraries and packages that allow beginners to keep building on a “pre-built” framework,
    thus improving the workflow management. Moreover, the python language on Neural Network is also used to build our Analysis Tool and Virtual Assistant as
    these features are Artificial Intelligence (Machine Learning).</p><p>The flask application will render the html templates and display them on the localhost
    server. Additionally, the analyzed data obtained from the user will be stored on the database for further assisting during the consultation with the doctor.
    The initial plan was to let the patient book an appointment for a consultation session with the certified specialists after making a payment, however, the
    appointment booking feature is not accessible and the payment gateway has not been implemented.</p>
    </li>
    </ul>
  </li>
</ol>

Add the local files to GitHub repository
Copy-paste the following command in Git:<br>
```bash
  git add .
```

Commit the updates to GitHub repository
Type the following commit in place of "commit_name" in Git:<br>
```bash
  git commit -m "commit_name"
```

Push the updates to main branch
Copy-paste the following command in Git:<br>
```bash
  git push -u origin main
```
