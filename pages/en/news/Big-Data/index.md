title: Big Data
date: 2014/10/06


##Interview: Ori Pekelman, Big Data track leader


**Big Data, what is it?**

In a way, all data these days is big, or potentially big, simply because the standard technological stack (well, for those not stuck in the 90s) is starting to support this; You know, one of the rules of computing is that disk spaces occupation is always expressed in percentage never in absolute terms.. and that it is always above 90%.. even if your own data set is small..  when you want to apply Machine Learning techniques to it you often  want to combine it with external data sources (you can extract median income from a zipcode.. which may give you more interesting models for example), basically : "hybrid data makes all data big"... If you'd like the canonical definition of big data stays the same (whatever dataish thing you can't do on your laptop..) only today a laptop can have 8 cores and 32GO and terabyte of SSD...

So with DataGeeks the informal bunch organizing the track with Olivier Grisel, Sam Bessalah and others, we are about data, not just the big kind.. its just that today  everything is getting big; and from the multiple Vs that describe what big data is we are getting more and more interested in the Velocity V. We can do damn intelligent stuff with an enormous quantity of data, now we are learning how to do it in real time. A lot of the talks this year are going to be around that, how to mount large scale extremely nervous systems that are not only fast but that are also fault-tolerant allow fast iteration and produce real business value.  Some of the stuff that we covered in earlier years as half-futuristic will this time be shown with hindsight as real use cases that were implemented successfully; We won't be even talking much about Hadoop.. subjects will center around streaming with talks about Kafka and Storm  but as usual we will also have strong accent on the application of Machine Learning techniques at the scale and speed of these systems.



**What are the uses today and in the future?**

Again, we are beyond any specific use case. Anyone building a data system that can not scale (in time or in volume), is simply doing her job incorrectly. So for many it is going to be a big question of how do I transit my 90s era architecture to the current bare minimum. Not having a scalable infrastructure is going to put many companies at a serious competitive disadvantage. There will be those companies that are capable of doing dynamic real-time yield management and those whose prices will always be inadequate. There will be companies that apply machine learning algorithmes to supply chain management, and those that will simply get the products later. Some will be able to align their employee bonuses to the strategic goals of the company, some that will play it by the ear.

There is no specific domain.



**Any technological challenges to overcome?**

Of course, and many of the talks will focus on those. For example, Olivier Grisel will present a state of the art view on Machine Learning techniques... what can be used now, what is still science fiction.. we are far from resolving many of the algorithmic issues. But also operational and business ones.. I see companies building their "data lakes" to replace their datawarehouses... without really defining strategic goals, or trying to look how this plays over five years or a decade. 

Working with streams vs working with batches is a change of paradigme, it changes how we do fault-tolerance, how we debug and identify the stuff that goes wrong how we recover from disasters... as always technological challenges are also cultural ones, even HR ones. I am note sure the same structure that applied to doing BI over legacy databases still applies to running a myriad of "small" algorithms in complex topologies. We are basically at the end of one cycle (putting in the infrastructure) and at the beginning of another... which is to make it productive.



**As techno providers: "SMEs" and "big companies" what interactions? And as users?**

As providers its quite ehtnousiasting, small companies can make huge projects in the big data world, because there is so much automation you don't need an army, you need extreme expertise.. and you can see the smarter "big companies" turning to the numerous big data startups for an edge. Still it is nice to see the bigger providers also develop a sens for the domain (even though often enough they push towards the "big big data solutions" instead of finding the smallest project that might possibly work and provide immediate business value...  We must never forget that outside the traditional "enterprise" you have the tech giants that are an enormous source of innovation in the domain (be it Google, Amazon, Linked-In or IBM..).

Anyway, the balances has not yet tilted, and there is an enormous spaces to be occupied by SMEs and startups. We have not yet scratched the surface on what can be done in HR or Supply Chain Management, but also in marketing automation (and some of what we will be able to do soon enough is frankly frightening.. ). Let's not forget that the Big in Big Data is a close relative to the Big Brother one.



**In which way the Open Source ecosystem is important for the Big Data?**

Well, I can think of only a few solutions in the domain that don't have as a prefix "apache"; Big Data is very much an Open Source game, and I don't see any serious contenders from the proprietary world, anyway not on the infrastructure level. There will be providers in the "value added" chain, stuff around specific algorithmes (often coupled with proprietary data sources) and around "interconnects"; As always the "As A service" Crowd, which is becoming the more potent rival to Free software will be important (but most of them will run Open Source solutions in any case). Hey but nobody ever said there was no place for proprietary software. Well, as long as it stays the minority exception. There is a strong ethical reason we want to fight not only for open source but also for open data, because the advent of opaque systems with smart algorithms and an extreme amount of data on us (the proprietary data + as a service model) is not only going to be bad for our privacy, its going to have tangible effects on our livelihoods, on our place is society as it can introduce an extreme form of information asymmetry at a scale not seen before. It is possible that in this domain more then in others the actors of Free Software need to be more vigilant and by working with the other actors of freedom make sure we are not constructing the tools of our demise.


*Made by Laurent Séguin, French speaking Libre Software Users' Association President*
