using System;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Autodesk.Revit.UI.Selection;

public class Class1
{
    private Result CreateWorksets(Document document, List<string> worksets)
    {
        if (document.IsWorkshared && !document.IsModifiable)
        {
            using (TransactionGroup worksetGroup = new TransactionGroup(document))
            {
                try
                {
                    worksetGroup.Start("Create Worksets");
                    IList<Autodesk.Revit.DB.Workset> userWork = UserWorksets(document);
                    foreach (Autodesk.Revit.DB.Workset k in userWork)
                    {
                        if (k.Name == "Workset1")
                        {
                            using (Transaction worksetTransaction = new Transaction(document))
                            {
                                worksetTransaction.Start("Create Workset: New Name");
                                WorksetTable.RenameWorkset(document, k.Id, "Your New Name as a String!");
                                worksetTransaction.Commit();
                            }
                        }
                    }
                    worksetGroup.Assimilate();
                    return Result.Succeeded;
                }
                catch (Autodesk.Revit.Exceptions.InvalidOperationException ex)
                {
                    return Result.Failed;
                }
            }
        }
        else
        {
            return Result.Cancelled;
        }
    }
    internal static IList<Autodesk.Revit.DB.Workset> UserWorksets(Document doc)
    {
        IList<Autodesk.Revit.DB.Workset> elements;
        using (FilteredWorksetCollector fwc = new FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset))
        {
            elements = fwc.ToWorksets();
        }
        return elements;
    }
}
