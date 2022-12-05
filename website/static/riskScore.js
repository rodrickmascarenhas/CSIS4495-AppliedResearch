var numericalValues = new Array();
   numericalValues["burnYes"]= 3;
   numericalValues["burnNo"]= 0;
   numericalValues["burnTan"]= 1;
   numericalValues["moleYes"]= 3;
   numericalValues["moleFew"]= 2;
   numericalValues["moleNo"]= 0;
   numericalValues["familyYes"]= 2;
   numericalValues["familyNo"]= 0;
   numericalValues["simYes"]= 1;
   numericalValues["simNo"]= 0;
   numericalValues["Thyroid"]= 1;
   numericalValues["BloodInfection"]= 1;
   
   function getburnScore(){
   var scoreBurn = 0;
   var form = document.forms["form"];
   var burn = form.elements["skinBurn"];
   for(var i=0; i<burn.length; i++)
   {
      if(burn[i].checked)
      {
      scoreBurn = numericalValues[burn[i].value];
      break;
      }
   }
   return scoreBurn;
   };

   function getMoleScore()
   {
   var moleScore = 0;
   var form = document.forms["form"];
   var mole = form.elements["skinMole"];
   for(var i=0; i<mole.length; i++)
   {
   if(mole[i].checked)
   {
   moleScore = numericalValues[mole[i].value];
   break;
   }
   }
   return moleScore;
   };
   function getFamScore()
   {
   var scoreFam = 0;
   var form = document.forms["form"];
   var fam = form.elements["familyHistory"];
   for(var i=0; i<fam.length; i++)
   {
      if(fam[i].checked)
      {
      scoreFam = numericalValues[fam[i].value];
      break;
      }
   }
   return scoreFam;
   };
   function getdiseaseScore()
   {
   var scoredisease ;
   var form = document.forms["form"];
   var disease = form.elements["simDisease"];
   for(var i=0; i<disease.length; i++)
   {
      if(disease[i].checked)
      {
      scoredisease = numericalValues[disease[i].value];
      break;
      }
   }
   return scoredisease;
   };

   function getTotal(){
   var totalScore = getburnScore() + getMoleScore() + getFamScore() + getdiseaseScore();
   result = document.querySelector('#result')
   result.value = totalScore;
   }
   //result1=document.write(result.style.fontweight);