Arnaud Tadonkeng
Professor Huixin Wu
Class Number
11/16/2026

# Report: The Benefits of Comprehensive Testing in Software Development
The benefits ot comprehensive testing in software development is being able to catch bugs early, basically when their cheap, it also allows you to make changes to code with confidence that you wont permenantely break the foundation of the code whatsoever, it also allows you to document the codes behavior while allowing for different kinds of tests and better designs for the code overrall.

## Before and After: Results Summary

* What was the initial test coverage? 
The initial test coverage was 85% coverage 
* What is the final test coverage you were able to achieve? 
while the final test coverage was somewhere like 100% I believe...
* How many tests did you end up having?
 I ended up with around 114 tests ran in my code 

## Untested Code: Effects

* Were you able to understand all features and different use cases of the code without the tests?
The routes and models showed me the main behavior but I couldn’t tell how the code handled unusual situations. The code didn't make it obvious so I had to guess.
* What did you think of having to test the API manually? 
Manual testing was so slow and annoying because I had to type out a request for every single check I made. 
* What was the result of having few tests on your understanding of the API?
With so few tests, I had gaps in my understanding of how the API worked, so later down the line I found genuine problems that I hadn't seen and caused bugs to be hidden until they popped up.
## Adding Tests

* How did you go about adding more tests to the code?
I read the codes in the starter test file then I ran a coverage report to find unexecuted lines and completed the unfinished unit tests 
* What is the difference between a unit test and an API test? Do they bring different values?
A unit test checks a small piece of code by itself while a API test sends a HTTP request to a  Flask’s test client to check the status code and JSON response, so it verifies that everything works together the way it was intended.
## Automation

* What were the benefits of automating test coverage?
Being able to run automatically on every push and pull request was honestly a godsend, since I didn't have to go back and forth to remember to run them myself and allows easy transition from the codespace in class to my visual studio code desktop applicatio at home. Also allowing any errors to be solved before publishing between either device.
## New Features

* What was your experience like having to add new features when you tested baseline code?
It was indded smoother then working without test but dear god the amount of errors I encontered still was genuinely just an ungodly amount 
* Did it give you any feeling of security when trying out new features?
Yes, I felt much safer making changes because the tests acted as a safety net.

## Future

* What do you hope to takeaway from the experience having to write tests?
I honestly hope to incorporate testing into more of my projects and allow coverage to be high from the beginning so that I don't have technical debt piling up. Most importantly I learned that good test allows for quick code changes without ruining the experience/webpage for the customers.
