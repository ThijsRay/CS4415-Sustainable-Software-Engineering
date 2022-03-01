<!--- 
Introduction:
Billion dollar industry
Ads on websites needed, but what is the impact on power consumption
Not only important for mobile websites (more screen real estate, more possibilities for ads)
reference to papers
--->
Showing advertisements is one of the key ways to earn money with a website. With the still ongoing digitalization of our society, [the online advertisement industry is growing along with it](https://www.statista.com/statistics/542808/net-online-advertising-market-revenue-in-the-netherlands-by-channel/). Loading the advertisement banners, logo's and small video clips do take time and energy to load onto a web page. In this blog post we take a look of the extra power consumption needed to load these advertisements. In [previous work](https://dl.acm.org/doi/10.1145/3372799.3394372) there have already been efforts to determine the power consumption of smart phones. However with the relatively more screen real-estate to fill, advertisements take up more space on the screens on computers.

<!--- 
Setup:
What did we turn off
Which resources did we use (Jouleit)
Time between tests
Repetitions
--->
Blocking advertisements on computers can be done by using an ad blocker like [uBlock](https://github.com/gorhill/uBlock/), which we used to load websites without the advertisements. In combination with the use of selenium, we were able to automate the visit of different websites, such that the experiments could be repeated XX times. With the [jouleit](https://github.com/powerapi-ng/jouleit) script from powerapi, the power consumptions during these website visits was measured. Now we just need to find some interesting websites to measure the power consumption of. We came up with the following list of websites, ranging from no advertisements at all to a lot of ads on a single page.

| Website | Ad intensity | # of requests |
| --- | --- | --- |
| Wikipedia | No ads | 0 (0%) |
| nu.nl | Many ads | 12 (7%) |
| Sparknotes | No ads | 7 (16%) |
| Deutsche Well | | 11 (7%) |
| Hackernews | No ads | 0 (0%) |
| Stackoverflow | | 2 (7%) |
| New York Times | | 15 (10%) |
| Reddit | | 32 (3%) |

We decided to not preheat the system as normally is done in such tests, since the preheating is not done in regular use of the webbrowser. A user normally loads website one by one, therefore the CPU would not be pre-heated in a regular scenario.


<!--- 
Results & Graph(s):
Is it a Normal distribution
Show stanadard deviation

--->

<!--- Image of with and without ads (boxplot and/or violin plot) --->
![Large boxplot comparing adblocker to no adblocker](results/boxplot-complete.png)
<!--- 
Discussion:
What went right 
where can the tests be improved  
What is the impact on society?
--->

<!---
Conclusion:
How many kilometers can we ride if we do a 1000 page loads?
--->


Would you like to reproduce the work we did? Use the following package of code we used to get this data.

Written by: Katja Schmahl & Thijs Raymakers & Jeffrey Bouman
