local chapter = 0
local section = 0
local subsection = 0

function Header(el)
    if el.level == 2 then
        chapter = chapter + 1
        section = 0
        subsection = 0
        el.content:insert(1, pandoc.Str(chapter .. ". "))
    elseif el.level == 3 then
        section = section + 1
        subsection = 0
        el.content:insert(1, pandoc.Str(chapter .. "." .. section .. ". "))
    elseif el.level == 4 then
        subsection = subsection + 1
        el.content:insert(1, pandoc.Str(chapter .. "." .. section .. "." .. subsection .. ". "))
    end
    return el
end
