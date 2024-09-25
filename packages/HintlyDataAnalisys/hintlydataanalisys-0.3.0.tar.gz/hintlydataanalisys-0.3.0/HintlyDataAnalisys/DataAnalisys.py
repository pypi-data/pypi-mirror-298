from enum import Enum
#Variables
intrepunctions = [".", ",", ":", ";", "?", "!", "\""]
whiteSigns = [" ", "  ", "\n", "\f"]

# Enums
class FilterType(Enum):
    Filter = "10294857630"
    Count = "85250958238"
class NormalizeType(Enum):
   DeleteInterpunctions = "023402839502938"
   LowText = "03950-1938509"
   DeleteWhiteSigns = "49582938598208745"
# Classes
class Math():
  def Mean(analisysData:list):
    srednia = 0
    srednia = sum(analisysData)
    return srednia/len(analisysData)
  def Difference(a, b):
    difference = b/a
    difference = difference*100
    return difference-100
  def Normalize(analisysData:list, normalizeNumber:int):
    najwieksza = 0
    for element in analisysData:
      if element > najwieksza:
        najwieksza = element
    position = 0
    for position in range(len(analisysData)):
      analisysData[position] = analisysData[position]/(najwieksza/normalizeNumber)
    return analisysData
  def MakeInt(value:float, divideNumber:int):
    return round(value-divideNumber,0)
  def AbsoluteDifference(a,b):
    return abs(a-b)
  def AbsoluteIntPercentDifference(a, b):
    return abs(Math.MakeInt(Math.Difference(a,b)))
  def WeightedAverage(analisysData=[],weights=[]):
    score=[]
    for position in range(len(analisysData)):
      for weight in range(weights[position]):
        analisysData.insert(analisysData[position]+weight, analisysData[position])
    return sum(analisysData)/len(analisysData)
  def NumberRepeat(numbers:list) -> dict:
        nums = {}
        for liczba in range(len(numbers)):
            if numbers[liczba] in nums:
                nums[numbers[liczba]] +=1
            else:
               nums[numbers[liczba]] = 1
        

        return nums
  def PercentNumberChance(numbers:list) -> dict:
        chance = {}
        repeats = Math.NumberRepeat(numbers)
        suma = sum(repeats.values())
        for i in range(len(numbers)):
           if numbers[i] not in chance:
            chance[numbers[i]] = (repeats.get(numbers[i])/suma)*100
        return chance
#class Finance():
    
    # def FinancialAngle(amounts:list, max_change:int):
    #     angles = []
    #     for i in range(1, len(amounts)):
    #         start_amount = amounts[i - 1]
    #         end_amount = amounts[i]
    #         angle = 180 * ((end_amount - start_amount) / max_change)
    #         angles.append(max(0, min(angle, 180)))
    #     return angles
    
class Text():
  def CountInrerpunctions(text:str) -> dict:
      data = {}
      for i in range(len(intrepunctions)):
         if intrepunctions[i] in text:
            data[intrepunctions[i]] = text.count(intrepunctions[i])
      return data
  def CountSigns(text:str, lowerSigns:bool) -> dict:
    data = {}
    signs = []
    if lowerSigns:
      for i in range(len(text.lower())):
          if text[i].lower() not in signs:
            data[text[i].lower()] = 1
            signs.append(text[i].lower())
          else:
            data[text[i].lower()] += 1
      return data
    else:
      for i in range(len(text)):
        if text[i] not in signs:
          data[text[i]] = 1
          signs.append(text[i])
        else:
          data[text[i]] += 1
      return data
  def CountWord(text:str,word:str) -> int:
  
     text = text.lower()
     word = word.lower()
     return text.count(word)
  def FilterWordsWithSign(text:str, sign:str,filterType:FilterType) -> dict:
    result = {}
    if filterType == FilterType.Count:
      result["count"] = Text.CountWord(sign)
      return result
    elif filterType == FilterType.Filter:
       newText = text.lower().replace(sign.lower(), "")
       result["filter"]  = newText
       return result
    else:
      return ValueError
  #def GetWordFrequency(text:str) -> dict:
  def NormalizeText(text:str, normalizeType:NormalizeType):
    result = ""
    if normalizeType == NormalizeType.DeleteInterpunctions:
      for i in range(len(intrepunctions)):
        text = text.replace(intrepunctions[i], '')
      result = text

    elif normalizeType == NormalizeType.LowText:
      result = text.lower()
    elif normalizeType == NormalizeType.DeleteWhiteSigns:
      for i in range(len(whiteSigns)):
        text = text.replace(whiteSigns[i], '')
      result = text
    return result
    # Zamieniamy wiadomość na małe litery i dzielimy na słowa
    slowa_w_wiadomosci = wiadomosc.lower().split()

    pozytywne = 0
    negatywne = 0

    # Sprawdzamy, ile słów z wiadomości znajduje się w słownikach
    for slowo in slowa_w_wiadomosci:
        if slowo in slowa_pozytywne:
            pozytywne += 1
        elif slowo in slowa_negatywne:
            negatywne += 1

    # Ustalamy ton na podstawie liczby znalezionych słów
    if pozytywne > negatywne:
        return "Radosny"
    elif negatywne > pozytywne:
        return "Zły"
    else:
        return "Neutralny"