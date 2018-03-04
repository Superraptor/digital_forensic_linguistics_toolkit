## Inspiration

The field of digital forensic linguistics is influenced greatly by its sister field of forensic linguistics—the application of linguistics to legal issues. Examples of such usage include an appeal against the conviction of Derek Bentley the identification of Subcomandante Marcos, the Zapatistas' charismatic leader by Max Appedole, and, perhaps most famously, the identification of Theodore Kaczynski as the so-called "Unabomber" by James R. Fitzgerald.

In the digital world, anonymity is both a blessing and a curse. It allows discussion of ideas without fear of persecution, but also perpetuation of terrible crimes without fear of retribution. Digital forensic linguistics, like its sister field, uses idiosyncrasies of digital languages, programming languages specifically, to identify demographic information about individuals, such as gender, approximate age, and location.

## What it does

The digital forensic linguistics toolkit uses random sampling of GitHub users to create a dataset from which a model is extracted, ultimately connecting inputs (information about the user's programs) to outputs (demographic information about the user).

## How I built it

## Challenges I ran into

* Getting access to GitHub's API and Microsoft's Face API and not surpassing strict rate limits (couldn't afford to get banned)
* Downloading nearly 60 GB of GitHub repositories
* Parsing through those repositories quickly
* Picking a machine learning model

## Accomplishments that I'm proud of

* Not getting banned from any of the API systems I used!
* Using Microsoft's Face API successfully
* Getting any machine learning model to actually work
* Getting any kind of product done
* Predicting mustache presence (albeit poorly)

## What I learned

Usage of Microsoft's Azure Face API is relatively easy, but scarily accurate, even with low resolution faces. Additionally, natural language and programming language predictions are fairly easy given existing Python architectures.

Choosing a machine learning algorithm is an exceedingly complicated task. Different algorithms are best under certain conditions, and patterns you can could be due to various confounds or other factors. In short, when using machine learning methods, be extremely careful.

## What's next for Digital Forensic Linguistics

While the system boats some decent accuracy and explained variance scores, it is not complete, as there were several input types I considered, but did not end up having time to completely implement. Further, a complete review of machine learning methodologies was (understandably) rushed, leaving out several which could have been more useful than those utilized in the end.

Hopefully, the system will be able to begin identifying individuals who have written various infamous virus programs. This will be a true test of the idea's efficacy. Additionally, a much larger sample of programmers will be necessary to continue forward.
