import ollama


# Define the message to be processed
message = """
Hello Joe,

We hope you're still interested in finding your dream job at Ford Motor Company. If so, we invite you to see if this might be the one. Learn more about our new positions below:

ADAS Embedded Software Performance Engineer
Technical Expert - Electronic Module Assembly Verification for Full-Service Supplier Electronic Control Units
Digitalization & Transformation OrgCM Communication Specialist
Software Engineer
Exterior Systems Design & Release Engineer

See all opportunities

Sincerely,
Ford Talent Acquisition Team
"""

def get_response(message, subject):
  """
  This function generates a response for a given email message and subject.
  The response is based on a set of predefined patterns and examples.
  The format of the response is (|status--job_title--company_name--brief_reasoning|)

  Args:
      message (str): The email message content
      subject (str): The email subject line

  Returns:
      str: The generated response
  """
  
  prompt = f""" You're AI assistent, and will organising my mail, by telling the mail status (rejected \ need action \ applied \ promotional \ personal\ job opportunities) or need further action by the user for that mail, additional information needed are job title if any otherwise `None`, and company name if not than `None`,  
  please note : the status are telling user about the mail status, such as, `need action` means that important task pending and need attention or selected for job, please not attach this status to advertising messages  or job application confirmation messages, where as applied means the mail is for confirmation that application is submitted succefully and can visit career page or look for message from company, rejected means you are no longer under consideration for the role, personal email means emails send by individual person can be HR or any other person personally,
  job opportunities status if the message recommends about the new job opportunities or openings and lastly promotional is if companies advertising or asking subscriptions or random email not useful for the user as it is not important.
  your output format `should` be in this way : '(|status--job_title--company name--brief reasoning|)`  and should not contain anything else no text nothing.
  Attaching few examples for your references, please understand the reasoning behind status before answering:
  Example 1:
  `
  subject : `Update on your Avanade application for FUTURE OPPORTUNITY - AI Engineer` 
  message : `Hi Joe,

  Thank you for your interest, however, we won't be moving ahead with your application at Avanade at this point.

  This does not have to mean the end of our journey together. There might be other opportunities here at Avanade that better match what we're both looking for. By keeping your job alerts active you can stay in touch with us and be the first to know about new roles that open up. 

  We wish you all the best for the future.

  Thanks
  Avanade Talent Acquisition Team`

  response: (|rejected--AI Engineer--Avanade--Avanade Update:
  Looks like this application wasn't a match, but don't ditch them yet!  Enable job alerts and snag the next awesome opportunity that pops up.|)`

  Example 2:
  `
  subject : `Your Amazon job application is incomplete`
  message : `Hi Joe,

  We noticed that your application for the position of Software Engineer II, Annapurna Labs (ID: 2650974) is incomplete.

  We can't consider you for the role until we've received your completed application.`

  response: (|need action--Software Egnineer 2--Amazon--Application alert! Annapurna Labs needs a few more things from your Software Engineer II application (ID: 2650974) before they can move forward.  Fill it up ASAP!|)`

  Example 3:
  `
  subject : `Outrider -- Thanks for your application!!`
  message: `Hi Joe!
  
  Thanks for your interest in Outrider! We received your application for the Engineer, Computer Vision & Machine Learning (3-month contract) role and we're delighted you'd consider joining our team.
  
  We'll review your application and contact you if there's a right fit for this role. If we don't choose to move forward at this time, please keep an eye on our jobs page, as we're growing and adding openings all the time.
  
  Thanks,
  
  The Outrider Team`

  response: (|applied--Computer Vision & Machine Learning Engineer--Outrider--Got the green light from Outrider to review your application for that 3-month CV & ML gig! Fingers crossed, but gotta keep an eye on their jobs page - seems like they're hiring like crazy!|)`

  Example 4:
  `subject : `The hits and misses in Delhivery's financials`
  message : `Dear Reader,

Delhivery, known for e-commerce logistics, expanded into B2B express, acquiring a player in 2021 for INR1,511 crore ahead of its 2022 IPO. Despite operational challenges post-merger, Delhivery has successfully navigated them.

Tech
Delhivery's B2B express logistics, affected post-Spoton acquisition, has rebounded well, but needs improvement in revenue and profitability.

Markets
Identifying potential 1000% return stocks in the current market involves monitoring low-valuation stocks showing profitability signs.

Auto + Aviation
A Maruti hatchback surpassed Alto as the bestseller in FY24.

Corporate Governance
Legal experts differ on the Tata Trusts vs Shapoorji Pallonji Group dispute.

Prime Decoder
Car manufacturers face historic inventory build-ups. What implications does this have for buyers?

Markets
Exide Industries has doubled investors' wealth in a year, with indications of further growth. Short-term traders may consider buying the stock for a target price of INR530 in two-three weeks.

GREENTOON OF THE DAY
ET Prime Team
Whatsapp Banner
Popular among readers

PS: For queries, email care@etprime.com. Unsubscribe here to stop receiving this newsletter or ensure delivery by adding the sender to your address book.

Did you enjoy today's newsletter?
`

  response: (|promotional--None--etprime--While this is informative, it's also promotional content as a newsletter.|)`

  Example 5:
  `
  subject : `Joe, we have received your application`
  message :  `Hello Joe,

We have received your application for Software Engineer II - Surgical Robotics. We are currently reviewing it and will reach out again as soon as there is an update. 

To track the status of your application, browse additional job opportunities or update your profile, you must create a candidate log-in account using this link.

Best Regards,
Medtronic Talent Team`

  response: (|applied--Software Engineer 2--Medtronic--Create a candidate log-in account to track your app status for the Surgical Robotics role at Medtronic. You can also browse other job openings and update your profile!|)
  `
  So similarly give the response for the following:,
  subject : `{subject}`
  message: `{message}`

  response: 
  """


  response = ollama.generate(model='llama3', prompt=prompt)
  return response["response"]

if __name__ == "__main__":
  # Test the llama
  print(get_response(message, "New job opportunities at Ford Global Career Site"))#"New jobs posted from jobs.hii-tsd.com"))