# Parking Lot Management System
**Goal** : to design of a University Parking Lot to issue permits for different categories of users and to regulate violations. 
The description of design required is as follows:
**Application Description**
The goal of this project is for you to develop a database application to help University Parking
Services (UPS) manage the campus parking lots and its users. The UPS issues parking permits
to employees, students and visitors and there are different eligibility constraints for parking
permits in the different lots as well as time restrictions for eligibility. In addition to the permits,
UPS issues tickets/citations for parking violations and collects fees for them. University students
and employees all have a univid (integer) which is a unique identifier for identifying them and
linking them to their vehicles as well as an attribute status that is either ‘S’ or ‘E’ or ‘A’
depending on whether a student or an employee or administrator (who is also an employee but
works with UPS).
**Parking lots** are identified by a unique name and an address and a zone’s designation that
determines who can park in the lot. Each zone has an identifier that is at most two characters
long: A, B, C, D, AS, BS, CS, DS, V. A parking lot can have a designation that includes multiple
zones. For example, a lot with zone designation A / B / C is a lot that combines three zones.
Zones fall under two categories: visitor and non-visitor (employee or student - we do not worry
about the UPS employee parking) parking zones. Zones A, B, C D are for employees, zones
with suffix ‘S’ - for students, V - for visitors.
A parking lot is made up of a set of spaces, each uniquely identified within the lot. In any lot that
has V as part of its zone designation, a set of spaces within that lot are dedicated to the V zone.
For example, say a lot is designated with A / B / V zones and there are 100 spaces in the lot,
spaces 90 - 100 may be dedicated to visitors zone V (spaces 1 to 89 in this case would be
considered both A and B spaces). Some spaces in a lot can have a dedicated type e.g. electric
vehicle or handicap, otherwise they are just regular spaces.
**Permits** fall broadly into two categories Visitor and NonVisitor. Each permit has a unique permit
identifier (8 character string length, begins with two digits for the year, one or two characters for
the zone, then a combination of numbers and characters for the remainder), zone identifier, a
car license number, start date, expiration date, expiration time, and a space type designation
e.g. “handicap” (default is “regular”). Nonvisitor permits are associated with a univid. For a
nonvisitor employee permit, one additional vehicle may be added to the permit (for a total of up
to 2 vehicles). For a visitor permit, the space number, start time and lot is also included in the
permit. The expiration date for employee permits is 11:59 pm, 12 months from start date and for
students it is 11:59 pm, 4 months from start date. The expiration date and time for a visitor’s
permit is computed as a function of request time plus the duration requested (some more details
of this is given below). Vehicle information associated with all permits include car manufacturer,
model, year, color, license plate (unique). While employee and student permits are assigned by
UPS employees, visitor’s permits are obtained by users invoking a procedure with appropriate
input GetVisitorPermit (Lot, duration, time beginning, type = default is standard, …). Below are
some functions that need to be supported. For all functions, we give a suggestion of inputs.
However, you are to think through and decide the final list of inputs and outputs for each
function. Below, we include a general description and which user role can execute it.
● ExitLot(): takes a permit number as input makes the status of a visitor space available
and computes any time overages for the reservation (in the case that a visitor
overstayed their booked amount of time). This can just be recorded as a time overage
for the permit.
● ChangeVehicleList(): this is to allow university users (employees) modify the vehicles on
their permit. They may remove or add vehicles. However, note the students can only
have one vehicle on a permit at a time, employees up to 2. The input to this should be
the permit number and univid (use for verifying if the correct user is making the
modification)
**The following are some rules and restrictions concerning permits and their usage in lots.**
1. To park in a lot, a user’s permit must have as its zone, one of the zones designated for
that lot. For example, a lot with zone designation A / B / C allows users with permits
either A, B or C.
2. Employees can have only one permit which allows them to park in any of the regular
spaces in a lot that includes their permit’s zone as one of its designation (but in the
dedicated visitor spaces region). Employees may also park in a zone designated for
students (S), but students cannot park in employee zones except after work hours i.e.
after 5pm.
3. A visitor permit allows a specific car in a specific visitor space and must include the
appropriate special type designation to park in dedicated type visitor spaces like for
electric cars. A visitor permit becomes invalid for any parking after permit expiration time.

**Citations** are issued to vehicles by UPS employees that violate parking regulations (the process
of issuing is discussed below). A citation includes a unique citation number, car license number,
model, color, date, lot, time, violation category, appropriate fee for the category and payment
due date (which is usually 30days after citation date). A citation also has a status which is paid
or unpaid. When it is initially issued, status is unpaid. The following are the categories and fees:
● Invalid Permit ($20)
● Expired Permit ($25)
● No Permit ($40)
IssueCitation () is a procedure that generates with appropriate information as described above.
A citation should alert the user via a notification. No integration with mail or sms is required.
However, notification should be achieved by inserting a tuple in a “notifications” table. The
structure of such a table is at your discretion but should include just basic information including
the contact information which for university entities it is their univid and for visitors we will
assume they include a phone number when requesting a permit.
Anyone can pay their citation by invoking the PayCitation ( ) procedure. (For our purposes, all
this citation will do is change the status of citation from unpaid to paid).
The administrators of the system (i.e. university employees in the UPS and are designated ‘A’)
have a few functions that they can perform.
● AddLot (... ): This function should take lot identifier and address of lot, number of spaces
in lot, beginning space number, initial zone designation (single zone initially).
● AssignZoneToLot (...):
● AssignTypeToSpace ( ...…. ):
● AssignPermit (univid, type, zone, ...…. ): assigns a permit to user with univid for parking
zone given in input and type (default is used if no input is given). Things like expiration
etc are computed based on the description given earlier.
● CheckVValidParking (CurrentTime, Date,Space#, Lot, License#): checks if car has valid
permit in visitors lot.
● CheckNVValidParking(time, permit#): checks valid parking in nonvisitor parking lot.

**User Interfaces** assume that your system has a main entry screen where users can select an
option of what role they want to play (admin, university user, visitor). Then, for each role, the list
of functions that they can perform will be listed and a user can select which function they want
to perform. University users should have a login step before their functions are displayed.
(Visitors should not need to log in because they dont have univids. Their functions should be
available once they choose that role). These user interfaces do not have to be graphical user
3
interfaces (but if you wish to do so that’s fine). A menu driven list e.g. numbered list of options
and users selecting the corresponding number for the option they want, should suffice.
For example, one the main screen you may present options like
1. UPS Admin Role
2. Employee Role
3. Student Role

