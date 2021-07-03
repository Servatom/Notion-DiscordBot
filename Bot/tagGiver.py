def giveTags(args):
    url = args[0]
    #Tag provided
    final_tag = []
    list_of_tags = []
                    
    #Multiple
    for tag in args[1:]:
        #Adding the arguments to list_of_tags
        list_of_tags.append(tag)
                    
        for tag in list_of_tags:
            #Splitting the arguments to get the tags
            tag_list = tag.split(",")
            for single_tag in tag_list:
                if(single_tag.strip() == ""):
                    continue
                #Appending tag to the final_tag dict
                final_tag.append({"name": single_tag.strip().lower(), "color": "default"})

    #For pdf files PDF tag
    if(".pdf" in url):
        final_tag.append({"name": "pdf", "color": "default"})
    
    print(final_tag)
    return final_tag

def getSearchTags(args):
    final_tag = []
    list_of_tags = []
                    
    #Multiple
    for tag in args:
        #Adding the arguments to list_of_tags
        list_of_tags.append(tag)
                    
        for tag in list_of_tags:
            #Splitting the arguments to get the tags
            tag_list = tag.split(",")
            for single_tag in tag_list:
                if(single_tag.strip() == ""):
                    continue
                #Appending tag to the final_tag dict
                final_tag.append({"property": "Tag", "multi_select": {"contains": single_tag.strip().lower()}})
    return final_tag
