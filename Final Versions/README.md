Final versions of code and results used to support and validate theory. 

Algorithm details:

1. **Basic Algorithm**:
 <img width="579" height="351" alt="image" src="https://github.com/user-attachments/assets/cf07baed-eb60-4cd9-8d09-29bcdc08de44" />

 
2. **Proposed Analogy of GA with Human Thinking**:
<img width="300" height="452" alt="image" src="https://github.com/user-attachments/assets/3620bcc7-fc5a-47e1-8a7c-d2dfd3afede5" />


3. **Modification to GA**:
- One difference between classic GA and human thinking is that, when mind traverses between thoughts, it learns from the previous thoughts, which is used while creating new thoughts.
- This Learning factor is added in the GA with the Learning Crossover Operator. 
- The fitter thoughts from previous populations can be stored and knowledge can be extracted out of them. 
<img width="348" height="542" alt="image" src="https://github.com/user-attachments/assets/977320b8-81e8-4225-89ef-a771a99b9b57" />


4. **TSP implementation of Modification**:
- Previously generated fitter individuals are stored and common subtours are extracted out of them.
- These common subtours are given to the Learning Crossover operator which uses them to create new individuals. 
- These new individuals are then given to the remaining operators of GA for further actions. 
<img width="575" height="246" alt="image" src="https://github.com/user-attachments/assets/65e9a8f4-ec1a-4825-901f-39f19ea4126e" />


5. **Results**:
- The paper proposes a theory of simulation and the goal was to check the feasibility. 
- The modification was not implemented with the goal of improving the performance of GA, but still it was compared with basic and existing GA, to understand its performance. 
- It is found that modified GA works better over small number of cities, both in case of basic and existing GA.
- This is so, because, the modification is added to the basic version of GA, and the version is not enhanced to work better on greater population. The modified GA increases the population more than the basic GA, which degrades its performance for more cities. 
- But this issue can be handled with certain additions to make modified GA better.
<img width="550" height="234" alt="image" src="https://github.com/user-attachments/assets/f01a2652-4e83-46d5-b70a-070f15379402" />
<img width="560" height="204" alt="image" src="https://github.com/user-attachments/assets/3320e717-afeb-49f8-8762-1578b6e5de57" />

