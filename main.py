 import arcpy

def display_menu():
    print("Spatial Join Menu:")
    print("1. Select target feature class")
    print("2. Select join feature class")
    print("3. Choose fields to keep from join feature class")
    print("4. Perform spatial join")
    print("5. Exit")

def perform_spatial_join(target_fc, join_fc, output_name, spatial_relationship, field_mappings):
    arcpy.SpatialJoin_analysis(target_fc, join_fc, output_name, join_operation="JOIN_ONE_TO_ONE",
                               join_type="KEEP_ALL", match_option=spatial_relationship, field_mapping=field_mappings)
def main():
    target_fc = ""
    join_fc = ""
    output_name = ""
    spatial_relationship = ""
    field_mappings = ""

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            target_fc = input("Enter the path to the target feature class: ")
        elif choice == "2":
            join_fc = input("Enter the path to the join feature class: ")
        elif choice == "3":
            if not join_fc:
                print("Error: Join feature class must be selected first.")
                continue

            field_mappings = arcpy.FieldMappings()
            join_fields = arcpy.ListFields(join_fc)

            print("Available fields in the join feature class:")
            for field in join_fields:
                print(field.name)

            field_choices = []
            while True:
                field_choice = input("Enter the field name to keep from the join feature class (or 'done' to finish): ")
                if field_choice.lower() == "done":
                    break
                elif field_choice.strip() == "":
                    print("Error: Field name cannot be empty.")
                    continue
                elif field_choice not in [field.name for field in join_fields]:
                    print("Error: Invalid field name.")
                    continue
                field_mapping = arcpy.FieldMap()
                field_mapping.addInputField(join_fc, field_choice)
                field_mappings.addFieldMap(field_mapping)
                field_choices.append(field_choice)

            print("Fields selected from the join feature class for spatial join: ", field_choices)

        elif choice == "4":
            if not target_fc or not join_fc:
                print("Error: Target and join feature classes must be selected first.")
                continue
            if not field_mappings:
                print("Error: Field mappings must be selected first.")
                continue

            spatial_relationship = input("Enter the spatial relationship (INTERSECT, CONTAINS, WITHIN, etc.): ")
            output_name = input("Enter the name of the output feature class: ")
            output_fc = arcpy.env.workspace + "\\" + output_name

            perform_spatial_join(target_fc, join_fc, output_fc, spatial_relationship, field_mappings)
            print("Spatial join completed. Output feature class created.")

        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
