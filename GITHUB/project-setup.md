# Projects

One GitHub Project per venture/product. Three views of the same issues:

| View | Layout | Filter |
|------|--------|--------|
| Roadmap | Roadmap | Type = Epic |
| Sprint | Board | Current Iteration |
| Defects | Board or Table | Type = Bug |

PO does not pick a second project. Bugs are not a separate project.

Sprint = Iteration field. Status = Project Status (not labels).

Create the empty project: `workitems.py setup-project --title "Venture board"`
Then finish views in the UI (ONCE.md). Mark as template: `gh project mark-template N --owner OWNER`.
