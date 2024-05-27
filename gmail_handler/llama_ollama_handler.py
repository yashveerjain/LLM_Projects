import ollama
# response = ollama.chat(model='llama3', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])

message = """
 Hello Yashveer,

You might be a great fit for the new positions we just posted! We hope you're still interested in finding your dream job at Ford Motor Company. If so, we invite you to see if this might be the one. Learn more here:

ADAS Embedded Software Performance Engineer
Technical Expert - Electronic Module Assembly Verification for Full-Service Supplier Electronic Control Units
Digitalization & Transformation OrgCM Communication Specialist
Software Engineer
Exterior Systems Design & Release Engineer
 
See all opportunities
 
Sincerely,
Ford Talent Acquisition Team 
"""
# message = """ 	
# ello yashveer,

# Thank you for joining HII's Talent Community on 2/11/24 and requesting notifications of available career opportunities. We are happy you have decided to build your career with HII’s Mission Technologies division!

# Your job alert request matched the following openings:
# Event Technical Lead - Virginia Beach, VA, Virginia, United States
# Project Manager (ITSIS) - 19148 - Virginia Beach, VA, Virginia, United States
# Subcontracts Administrator (Subcontracts Administrator 2) - 17558 - Virginia Beach, VA, Virginia, United States
# Contract Administrator (Contract Administrator 2) - 18292 - Virginia Beach, VA, Virginia, United States
# Pipefitter - 19107 - Virginia Beach, VA, Virginia, United States


# Search for and apply for other opportunities by visiting us at hii.com/careers.
# """

def get_response(message, subject):
  prompt = f""" You're AI assistent, and will organising my mail, by telling the mail status (rejected \ need action \ applied \ promotional \ personal\ job opportunities) or need further action by the user for that mail, additional information needed are job title if any otherwise `None`, and company name if not than `None`,  
  please note : the status are telling user about the mail status, such as, `need action` means that important task pending and need attention or selected for job, please not attach this status to advertising messages  or job application confirmation messages, where as applied means the mail is for confirmation that application is submitted succefully and can visit career page or look for message from company, rejected means you are no longer under consideration for the role, personal email means emails send by individual person can be HR or any other person personally,
  job opportunities status if the message recommends about the new job opportunities or openings and lastly promotional is if companies advertising or asking subscriptions or random email not useful for the user as it is not important.
  your output format `should` be in this way : '(|status--job_title--company name--brief reasoning|)`  and should not contain anything else no text nothing.
  Attaching few examples for your references:
  Example 1:
  `
  subject : `Update on your Avanade application for FUTURE OPPORTUNITY - AI Engineer` 
  message : `Hi Yashveer,

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
  message : `Hi Yashveer,

  We noticed that your application for the position of Software Engineer II, Annapurna Labs (ID: 2650974) is incomplete.

  We can't consider you for the role until we've received your completed application.`

  response: (|need action--Software Egnineer 2--Amazon--Application alert! Annapurna Labs needs a few more things from your Software Engineer II application (ID: 2650974) before they can move forward.  Fill it up ASAP!|)`

  Example 3:
  `
  subject : `Outrider -- Thanks for your application!!`
  message: `Hi Yashveer!
  
  Thanks for your interest in Outrider! We received your application for the Engineer, Computer Vision & Machine Learning (3-month contract) role and we're delighted you'd consider joining our team.
  
  We'll review your application and contact you if there's a right fit for this role. If we don't choose to move forward at this time, please keep an eye on our jobs page, as we're growing and adding openings all the time.
  
  Thanks,
  
  The Outrider Team`

  response: (|applied--Computer Vision & Machine Learning Engineer--Outrider--Got the green light from Outrider to review your application for that 3-month CV & ML gig! Fingers crossed, but gotta keep an eye on their jobs page - seems like they're hiring like crazy!|)`

  Example 4:
  `subject : `AI and your tech career: 10-part article series.`
  message : `Welcome to "AI and Your Tech Career," Dice's 10-part article series walking through the basics of how to successfully integrate artificial intelligence and machine learning into your tech career journey.
  We'll cover everything from the most popular jobs and skills to non-technical roles in AI, industry applications, and more. You can build your dream tech career, and AI can help!

  Part 1: Unveiling AI Career Opportunities: Key Roles and Emerging Hybrid Jobs in Artificial Intelligence`

  response: (|promotional--None--Dice--While this is informative, it's also promotional content from Dice (a job search website).|)`

  Example 5:
  `
  subject : Yashveer, we have received your application
  message :  Hello Yashveer,

We have received your application for Software Engineer II - Surgical Robotics. We are currently reviewing it and will reach out again as soon as there is an update. 

To track the status of your application, browse additional job opportunities or update your profile, you must create a candidate log-in account using this link.

Best Regards,
Medtronic Talent Team

  response: (|job opportunities--Software Engineer 2--Medtronic--Create a candidate log-in account to track your app status for the Surgical Robotics role at Medtronic. You can also browse other job openings and update your profile!|)
  `
  So similarly give the response for the following:,
  subject : `{subject}`
  message: `{message}`

  response: 
  """

  # print(prompt)

  # print("================")
  # response_parts = ollama.generate(model='llama3', prompt=prompt, stream=True)

  # for response in response_parts:
  #   print(response["response"], end="",flush=True)

  # response = ollama.chat(model='llama3', messages=[
  #   {
  #     'role': 'user',
  #     'content': prompt,
  #   },
  # ])
  # print(response['message']['content'])

  response = ollama.generate(model='llama3', prompt=prompt)
  return response["response"]

if __name__ == "__main__":
  print(get_response(message, "New job opportunities at Ford Global Career Site"))#"New jobs posted from jobs.hii-tsd.com"))