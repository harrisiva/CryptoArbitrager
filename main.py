# Get the arguments from the user (refresh time, failsafe time, base, currency)
# 
# Get the endpoint names by using endpoint.keys() (print the number of combinations (or log for future reference))
# Create a table for each broker/endpoint
# Create the book table
# 
# Initialize the last update datetime variable
# Iterate while current_time=last_update + refresh_period (seconds)
#
#   Refreshing and DB Handling:
#   Iterate over the endpoints/broker
#   Create a database entry to the broker/endpoint table
#   Update the book table for the current endpoint/broker

#   Trading:
#   Perform the difference on the different combinations
#   Find the maximum difference
#   If the entry pair for the maximum difference both have a timestamp of that indicates that it was updated:
#       Perform the trade if it is within a failsafe period (s) from the update time
#       Log the trade time