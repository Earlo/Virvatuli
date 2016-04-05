
class english():
    NORMAL_ORDERED_SUFFIX = "th"
    SPECIAL_ORDERED_SUFFIX = {  "1":"st",
                                "2":"nd",
                                "3":"rd"}
    MONTHS = {  "1": "January",
                "2": "February",
                "3": "March",
                "4": "April",
                "5": "May",
                "6": "June",
                "7": "July",
                "8": "August",
                "9": "September",
                "10":"October",
                "11":"November",
                "12":"December"}

    WEEKDAYS = {    0: "Monday",
                    1: "Tuesday",
                    2: "Wednesday",
                    3: "Thursday",
                    4: "Friday",
                    5: "Saturday",
                    6: "Sunday"}

    def ordered_number(self, num):

        num_s = str(num)

        if ( num_s[-1] in self.SPECIAL_ORDERED_SUFFIX.keys() and not ( len(num_s) >= 2 and num_s[-2] == "1" ) ):
            suffix = self.SPECIAL_ORDERED_SUFFIX[ num_s[-1] ]
        else:
            suffix = self.NORMAL_ORDERED_SUFFIX

        return (num_s + suffix)

    def months(self,key):
        return self.MONTHS[key]

    def weekday(self,key):
        return self.WEEKDAYS[key]

    def date(self,d,m,y):
        day = self.ordered_number( d )
        month = self.months( m )
        year = str( y )
        string = day + " of " + month + " in " + year
        return string

