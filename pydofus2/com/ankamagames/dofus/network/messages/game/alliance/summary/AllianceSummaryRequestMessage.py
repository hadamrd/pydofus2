from pydofus2.com.ankamagames.dofus.network.messages.game.PaginationRequestAbstractMessage import \
    PaginationRequestAbstractMessage


class AllianceSummaryRequestMessage(PaginationRequestAbstractMessage):
    filterType: int
    textFilter: str
    criterionFilter: list[int]
    sortType: int
    languagesFilter: list[int]
    recruitmentTypeFilter: list[int]
    minPlayerLevelFilter: int
    maxPlayerLevelFilter: int
    hideFullFilter: bool
    followingAllianceCriteria: bool
    sortDescending: bool
    hideFullFilter: bool
    followingAllianceCriteria: bool
    sortDescending: bool

    def init(
        self,
        filterType_: int,
        textFilter_: str,
        criterionFilter_: list[int],
        sortType_: int,
        languagesFilter_: list[int],
        recruitmentTypeFilter_: list[int],
        minPlayerLevelFilter_: int,
        maxPlayerLevelFilter_: int,
        hideFullFilter_: bool,
        followingAllianceCriteria_: bool,
        sortDescending_: bool,
        offset_: int,
        count_: int,
    ):
        self.filterType = filterType_
        self.textFilter = textFilter_
        self.criterionFilter = criterionFilter_
        self.sortType = sortType_
        self.languagesFilter = languagesFilter_
        self.recruitmentTypeFilter = recruitmentTypeFilter_
        self.minPlayerLevelFilter = minPlayerLevelFilter_
        self.maxPlayerLevelFilter = maxPlayerLevelFilter_
        self.hideFullFilter = hideFullFilter_
        self.followingAllianceCriteria = followingAllianceCriteria_
        self.sortDescending = sortDescending_

        super().init(offset_, count_)
