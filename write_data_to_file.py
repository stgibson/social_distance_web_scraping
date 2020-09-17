class WriteDataToFile:
  def __init__(self, categories):
    self.categories = categories

  def writeToFile(self):
    data = [["Categories", "Name 1", "Name 2", "Phone", "Address 1", "Address 2"]]

    for category in self.categories:
      name = category["name"]
      locations = category["locations"]

      data.append([name])

      for location in locations:
          # write all locations under name
          names = []
          phone = None
          address1 = None
          address2 = None

          if "names" in location:
            names = location["names"]
          if "phone" in location:
            phone = location["phone"]
          if "address1" in location:
            address1 = location["address1"]
          if "address2" in location:
            address2 = location["address2"]

          # list of names, phone number, and address
          locationRow = [""]
          if len(names) == 1:
            locationRow.append(names[0])
            locationRow.append("")
          else:
            locationRow.append(names[0])
            locationRow.append(names[1])
          if phone:
            locationRow.append(phone)
          else:
            locationRow.append("")
          if address1:
            locationRow.append(address1)
          else:
            locationRow.append("")
          if address2:
            locationRow.append(address2)
          else:
            locationRow.append("")

          data.append(locationRow)

    self.tableToCsv(data, "social_distance_data.csv")

  def tableToCsv(self, data, fileName):
    '''
    This converts a two-dimensional array into a csv file.
    type data: List[List[str]]
    type fileName: str
    '''
    f = open(fileName, "w")
    # write each row on a separate line
    for row in data:
      # add comma before every item except first
      first = True
      for item in row:
        if first:
          f.write(item)
          first = False
        else:
          f.write("|")
          f.write(item)

      # after row, go to next line
      f.write("\n")